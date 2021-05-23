import {useEffect, useState} from "react";
import Link from '@material-ui/core/Link';
import Button from '@material-ui/core/Button';
import TextLoop from "react-text-loop";

export default () => {
  const [availableTickers, setAvailableTickers] = useState([]);

  useEffect(() => {
    fetch('/securities').then(res => res.json()).then(setAvailableTickers);
  }, [])

  const sampleTickers = ['TSLA', 'AAPL', 'PYPL', 'PLTR', 'NVDA', 'AMZN', 'MSFT'];

  return (
    <div>
      <h1>Welcome!</h1>
      <div style={{width: 800}}>
        <h2>To see an order book or live transaction log, please visit /order-book/
          <TextLoop
            springConfig={{ stiffness: 180, damping: 8 }}
            interval={1300}
          >
            {sampleTickers.map(ticker => <span key={ticker}>{ticker}</span>)}
          </TextLoop>
        </h2>
      </div>
      {availableTickers && <h3>
        Currently, tickers with data are:
      </h3>}
      <div style={{display: 'flex', flexDirection: 'row', justifyContent: 'center'}}>
        {availableTickers.map(ticker => (
          <Button size={'large'} style={{flex: 1, maxWidth: 75, color: 'black', backgroundColor: '#00df9a', margin: 10}} href={`/order-book/${ticker}`}>{ticker}</Button>
        ))}
      </div>
      <h2>
        You can also&nbsp;
        <Link style={{color: '#00df9a'}} href={'/order'}>
          place an order
        </Link>
      </h2>
      
    </div>
  );
}