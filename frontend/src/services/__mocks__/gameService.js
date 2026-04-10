// Manual mock: every named export exists so tests never see undefined after
// partial factory mocks clobber the module in the same Jest worker.
module.exports = {
  createGame: jest.fn(),
  listGames: jest.fn(),
  getGame: jest.fn(),
  joinGameById: jest.fn(),
  joinGameByCode: jest.fn(),
  matchmake: jest.fn(),
  startGame: jest.fn(),
  leaveGame: jest.fn(),
  getLeaderboard: jest.fn(),
  createGameWebSocket: jest.fn(),
  sendMove: jest.fn(),
  sendSelectPiece: jest.fn(),
  sendGameChat: jest.fn(),
  createGlobalChatWebSocket: jest.fn(),
  sendGlobalChat: jest.fn(),
};
