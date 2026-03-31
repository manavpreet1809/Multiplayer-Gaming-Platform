import React from 'react';
import './GameItem.css';
import Logo from '../../logo.svg';
/**
 * 
 * @param itemIcon uri of image to load in frame
 * @param ItemEndpoint endpoint to link to
 */
export default function GameItem({
    itemEndpoint,
    itemIcon
}) {
    return(
    <div className="game-item">
        <a href={itemEndpoint}><img src={Logo}></img></a>
    </div>
    )
}