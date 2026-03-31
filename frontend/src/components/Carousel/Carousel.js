
import GameItem from '../GameItem/GameItem.js';
import '../../index.css';
import './Carousel.css';
import Logo from '../../logo.svg';

export default function Carousel() {
    return(
    <div className="carousel-root">
        <div className='carousel-chess'>
            <img src={Logo}></img>
        </div>
        <div className="carousel-tictac">
            <img src={Logo}></img>
        </div>
        <div className='carousel-next'></div>
        <div className='carousel-prev'></div>
    </div>
    )
}