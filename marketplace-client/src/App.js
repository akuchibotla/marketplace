import React, {useState, useEffect} from 'react';
import OrderBook from './components/OrderBook';
import HomePage from './components/HomePage';
import socketIOClient from 'socket.io-client';
import PlaceOrder from './components/PlaceOrder';
import TransactionLog from './components/TransactionLog';
import CssBaseline from '@material-ui/core/CssBaseline';
import {ThemeProvider, createMuiTheme} from '@material-ui/core/styles';

function App() {
  const [orderBookData, setOrderBookData] = useState(null);
  const [transactions, setTransactions] = useState([]);
  const [ticker, setTicker] = useState(null);

  const [showHomePage, setShowHomePage] = useState(true);
  const [showOrderPage, setShowOrderPage] = useState(false);
  const [showOrderBook, setShowOrderBook] = useState(false)

  useEffect(() => {
    const currPath = window.location.pathname.split('/').slice(1);
    if (currPath.length === 1 && currPath[0] === 'order') {
      setShowHomePage(false);
      setShowOrderPage(true);
      setShowOrderBook(false);
      setTicker(null);
    }
    else if (currPath.length === 2 && currPath[0] === 'order-book') {
      setShowHomePage(false);
      setShowOrderPage(false);
      setShowOrderBook(true);
      setTicker(currPath[1]);
    } else {
      setShowHomePage(true);
      setShowOrderPage(false);
      setShowOrderBook(false);
      setTicker(null);
    }
  } ,[]);

  useEffect(() => {
    if (ticker) {
      const socket = socketIOClient('/order-book');
      socket.on('connect', () => {
        socket.emit('connection_event', {data: ticker});
      });
      socket.on('order_book_update', (json_data) => {
        const data = JSON.parse(json_data);
        setOrderBookData(data);
      });
      socket.on('order_match_event', (transactions) => {
        setTransactions(
          oldTransactions => [...transactions, ...oldTransactions]
        );
      })
      return () => {
        socket.close();
      }
    }
  }, [ticker]);

  const appStyle = {textAlign: 'center'};
  const containerStyle = {
    backgroundColor: 'black',
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center'
  };

  const theme = createMuiTheme({
    palette: {
      type: "dark",
      secondary: {
        main: '#00df9a'
      },
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div style={appStyle}>
        <div style={containerStyle}>
          {showHomePage && <HomePage />}
          {showOrderPage && <PlaceOrder />}
          {showOrderBook && (
            <>
              <h1>Order book for {ticker}</h1>
              <OrderBook data={orderBookData} />
              <TransactionLog data={transactions}/>
            </>
          )}
        </div>
      </div>
    </ThemeProvider>
  );
}

export default App;
