import GameItem from '../GameItem/GameItem';
import '../../index.css';
import './Carousel.css';
import Logo from '../../logo.svg';
import { useRef } from 'react';

export default function Carousel() {
    return(
    <div className='carousel'>
        <button className='carousel-next' 
            onClick={() => {         
                document.getElementById('carousel').scrollBy({left:1000,top:0,behavior:'smooth'});
            }}>
            &gt;
        </button>
        <button className='carousel-prev' 
            onClick={() => {         
                document.getElementById('carousel').scrollBy({left:-1000,top:0,behavior:'smooth'});
            }}>
            &lt;
        </button>
        <div id='carousel' className="carousel-root">
            <div className='carousel-chess'>
                <img src={Logo}></img>
            </div>
            <div className="carousel-tictac">
                <img src={Logo}></img>
            </div>
            <div >
                <img src={Logo}></img>
            </div>
        </div>
    </div>
    )
}