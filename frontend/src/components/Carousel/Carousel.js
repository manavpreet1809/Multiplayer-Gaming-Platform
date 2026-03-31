
import GameItem from '../GameItem/GameItem.js';
import '../../index.css';
import './Carousel.css';
import Logo from '../../logo.svg';
import { useRef } from 'react';

export default function Carousel() {
    const carouselRef = useRef(null);
    function scrollCarousel(direction) {
        const container = carouselRef.current;
        if (!container) return;
        const scrollAmount = container.clientWidth; // scroll by visible width

        container.scrollBy({
            left: direction === 'next' ? scrollAmount : -scrollAmount,
            behavior: 'smooth'
        });
    }
    return(
    <div className="carousel-root" ref={carouselRef}>
        <button className='carousel-next' onClick={scrollCarousel(100,'r')}></button>
        <button className='carousel-prev' onClick={scrollCarousel(100,'l')}></button>
        <div className='carousel-chess'>
            <img src={Logo}></img>
        </div>
        <div className="carousel-tictac">
            <img src={Logo}></img>
        </div>
    </div>
    )
}