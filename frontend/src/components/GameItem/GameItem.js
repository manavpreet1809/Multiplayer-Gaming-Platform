import React from 'react';
import './GameItem.css';
/**
 * 
 * @param {itemIcon} itemIcon uri of image to load in frame
 */
export default function GameItem({
    itemEndpoint,
    itemIcon
}) {
    <div className="game-item">
        <a href={itemEndpoint}><img src={itemIcon}></img></a>
    </div>
}