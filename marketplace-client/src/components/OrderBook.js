import React from 'react';
import SideOrderTable from './SideOrderTable';

export default ({data}) => {
  if (!data) {
    data = {'bids': [], 'asks': []}
  }

  const {bids, asks} = data;
  const containerStyle = {
    height: 500,
    width: '75%',
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-evenly',
    alignItems: 'stretch',
    backgroundColor: '#333',
  }

  return (
    <div style={containerStyle}>
      <SideOrderTable data={bids} key={'bids'} side={'Bid'}/>
      <SideOrderTable data={asks} key={'asks'} side={'Ask'} />
    </div>
  );
}