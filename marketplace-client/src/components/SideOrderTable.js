import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
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

const StyledTableRow = withStyles((theme) => ({
  root: {
    '&:nth-of-type(odd)': {
      backgroundColor: theme.palette.action.hover,
    },
  },
}))(TableRow);

export default ({data, side}) => {
  return (
    <TableContainer component={Paper} style={{flex: 1, margin: 3, overflowY: 'scroll'}}>
      <Table aria-label="simple table">
        <TableHead>
          <StyledTableRow>
            <StyledTableCell>{`${side} price`}</StyledTableCell>
            <StyledTableCell align="right">Volume</StyledTableCell>
            <StyledTableCell align="right">User</StyledTableCell>
            <StyledTableCell align="right">Timestamp</StyledTableCell>
          </StyledTableRow>
        </TableHead>
        <TableBody>
          {data.map((order) => (
            <StyledTableRow key={order.timestamp}>
              <StyledTableCell component="th" scope="row">
                ${order.price}
              </StyledTableCell>
              <StyledTableCell align="right">{order.volume}</StyledTableCell>
              <StyledTableCell align="right">{order.username}</StyledTableCell>
              <StyledTableCell align="right">{order.timestamp}</StyledTableCell>
            </StyledTableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};