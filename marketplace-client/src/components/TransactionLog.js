import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

const StyledTableCell = withStyles((theme) => ({
  head: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  body: {
    fontSize: 14,
  },
}))(TableCell);

const containerStyle = {
  height: 300,
  width: '70%',
  display: 'flex',
  flexDirection: 'row',
  justifyContent: 'space-evenly',
  alignItems: 'stretch',
}

const timestampStyle = {
    color: '#00df9a',
}

export default ({data}) => {
  return (
    <TableContainer component={Paper} style={containerStyle}>
      <Table aria-label="simple table">
        <TableBody>
          {data.map(({price, volume, security, payee, payer, timestamp}) => (
            <TableRow key={timestamp}>
              <StyledTableCell component="th" scope="row">
                <span style={timestampStyle}>({timestamp}):</span> {payee} received {volume} shares of {security} from {payer} at ${price}/share
              </StyledTableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}