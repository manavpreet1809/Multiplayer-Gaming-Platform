"""
Games repository — persists game results to MongoDB and provides
leaderboard / stats queries.

Collection: game_results
Document schema:
  {
    "_id":         game_id (str),
    "game_type":   "chess" | "tictactoe",
    "players":     [username, ...],
    "winner":      username | null   (null = draw),
    "result_type": "win" | "draw" | "forfeit" | "stalemate",
    "finished_at": datetime (UTC)
  }
"""

from datetime import datetime, timezone
from pymongo import IndexModel, ASCENDING, DESCENDING

from app.db.mongo import db

game_results_collection = db["game_results"]


async def create_game_indexes():
    await game_results_collection.create_indexes([
        IndexModel([("game_type", ASCENDING)]),
        IndexModel([("players", ASCENDING)]),
        IndexModel([("finished_at", DESCENDING)]),
    ])


async def save_game_result(
    game_id: str,
    game_type: str,
    players: list[str],
    winner: str | None,
    result_type: str,
):
    """Upsert a finished game result. Safe to call multiple times for the same game."""
    doc = {
        "_id": game_id,
        "game_type": game_type,
        "players": players,
        "winner": winner,
        "result_type": result_type,
        "finished_at": datetime.now(timezone.utc),
    }
    await game_results_collection.replace_one({"_id": game_id}, doc, upsert=True)


def _mmr(wins: int, losses: int) -> int:
    return 1000 + wins * 25 - losses * 20


def _tier(mmr: int) -> str:
    if mmr >= 1200:
        return "Platinum"
    if mmr >= 1000:
        return "Gold"
    if mmr >= 800:
        return "Silver"
    return "Bronze"


async def get_leaderboard(game_type: str) -> list[dict]:
    """Return ranked list of players for a given game type."""
    pipeline = [
        {"$match": {"game_type": game_type}},
        {"$unwind": "$players"},
        {
            "$group": {
                "_id": "$players",
                "wins":   {"$sum": {"$cond": [{"$eq": ["$winner", "$players"]}, 1, 0]}},
                "losses": {
                    "$sum": {
                        "$cond": [
                            {
                                "$and": [
                                    {"$ne": ["$winner", None]},
                                    {"$ne": ["$winner", "$players"]},
                                ]
                            },
                            1,
                            0,
                        ]
                    }
                },
                "ties": {
                    "$sum": {"$cond": [{"$eq": ["$result_type", "draw"]}, 1, 0]}
                },
            }
        },
    ]

    rows = []
    async for doc in game_results_collection.aggregate(pipeline):
        mmr = _mmr(doc["wins"], doc["losses"])
        rows.append({
            "username": doc["_id"],
            "wins":     doc["wins"],
            "losses":   doc["losses"],
            "ties":     doc["ties"],
            "mmr":      mmr,
            "tier":     _tier(mmr),
        })

    rows.sort(key=lambda r: r["mmr"], reverse=True)
    for i, row in enumerate(rows, start=1):
        row["rank"] = i

    return rows


async def get_user_stats(username: str) -> dict:
    """Return overall and per-game-type stats for a player."""
    pipeline = [
        {"$match": {"players": username}},
        {
            "$group": {
                "_id": "$game_type",
                "games_played": {"$sum": 1},
                "wins":   {"$sum": {"$cond": [{"$eq": ["$winner", username]}, 1, 0]}},
                "losses": {
                    "$sum": {
                        "$cond": [
                            {
                                "$and": [
                                    {"$ne": ["$winner", None]},
                                    {"$ne": ["$winner", username]},
                                ]
                            },
                            1,
                            0,
                        ]
                    }
                },
                "ties": {
                    "$sum": {"$cond": [{"$eq": ["$result_type", "draw"]}, 1, 0]}
                },
            }
        },
    ]

    game_stats = []
    total = {"gamesPlayed": 0, "wins": 0, "losses": 0, "ties": 0}

    async for doc in game_results_collection.aggregate(pipeline):
        mmr = _mmr(doc["wins"], doc["losses"])
        game_stats.append({
            "gameType":    doc["_id"],
            "gamesPlayed": doc["games_played"],
            "wins":        doc["wins"],
            "losses":      doc["losses"],
            "ties":        doc["ties"],
            "mmr":         mmr,
            "rank":        _tier(mmr),
        })
        total["gamesPlayed"] += doc["games_played"]
        total["wins"]        += doc["wins"]
        total["losses"]      += doc["losses"]
        total["ties"]        += doc["ties"]

    return {"generalStats": total, "gameStats": game_stats}