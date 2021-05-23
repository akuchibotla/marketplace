import React, {useEffect, useState} from 'react';
import Button from '@material-ui/core/Button';
import SendIcon from '@material-ui/icons/Send';
import TextField from '@material-ui/core/TextField';
import {makeStyles} from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  root: {
    '& .MuiTextField-root': {
      margin: theme.spacing(1),
      width: '25ch',
    },
  },
}));

export default () => {
  const classes = useStyles();

  const orderOptions = [
    {label: 'Buy order', value: 'buy'},
    {label: 'Sell order', value: 'sell'}
  ];

  const [orderType, setOrderType] = useState('buy');
  const [ticker, setTicker] = useState(null);
  const [tickerError, setTickerError] = useState(false);
  const [price, setPrice] = useState(null);
  const [priceError, setPriceError] = useState(false);
  const [volume, setVolume] = useState(null);
  const [volumeError, setVolumeError] = useState(false);
  const [username, setUsername] = useState(null);
  const [usernameError, setUsernameError] = useState(false);

  const disableSubmit =
    !ticker || tickerError ||
    !price || priceError ||
    !volume || volumeError ||
    !username || usernameError;

  useEffect(() => {
    setTickerError(ticker && (!/^[a-zA-Z]+$/.test(ticker) || ticker.length > 4));
  }, [ticker]);
  
  useEffect(() => {
    setPriceError(price && !parseFloat(price));
  }, [price]);

  useEffect(() => {
    setVolumeError(volume && !parseInt(volume));
  }, [volume]);

  useEffect(() => {
    setUsernameError(username && !/^[a-zA-Z]+$/.test(username));
  }, [username]);

  return (
    <>
      <h1>Place an order</h1>
      <form className={classes.root} noValidate autoComplete="off">
        <div style={{display: 'flex', alignItems: 'center'}}>
          <TextField
            select
            id='order-type'
            label="Order type"
            value={orderType}
            SelectProps={{
              native: true,
            }}
            onChange={event => {
              setOrderType(event.target.value);
            }}
            variant={'outlined'}
          >
            {orderOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </TextField>
          <TextField
            required
            id='security'
            label='Ticker'
            value={ticker}
            variant='outlined'
            error={tickerError}
            onChange={event => {
              setTicker(event.target.value)
            }}
          />
          <TextField
            required
            id='price'
            value={price}
            label='Price per share'
            variant="outlined"
            error={priceError}
            onChange={event => {
              setPrice(event.target.value)
            }}
          />
        </div>
        <div style={{display: 'flex', alignItems: 'center'}}>
          <TextField
            required
            id='volume'
            value={volume}
            label='Number of shares'
            variant="outlined"
            error={volumeError}
            onChange={event => {
              setVolume(event.target.value)
            }}
          />
          <TextField
            required
            id='username'
            label="Username"
            value={username}
            variant="outlined"
            error={usernameError}
            onChange={event => {
              setUsername(event.target.value.replace(/\s+/g, ''))
            }}
          />
          <Button
            style={{flex: 1, height: 50, marginInline: 2, color: disableSubmit ? 'gray' : 'lime'}}
            disabled={disableSubmit}
            variant='outlined'
            size='large'
            endIcon={<SendIcon />}
            onClick={() => {
              const securityTicker = ticker;
              const requestOptions = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  order_type: orderType,
                  price,
                  volume,
                  username
                })
              };
              fetch(`/order/${securityTicker}`, requestOptions).then(
                response => {
                  if (response.ok) {
                    alert(`Successfully placed order! You can see it at /order-book/${securityTicker}`);
                    window.location.reload();
                  }
                }
              );
            }}
          >
            Submit
          </Button>
        </div>
      </form>
    </>
  )
}