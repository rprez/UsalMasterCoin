// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.4;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract PuntosRecompensasCoin is ERC20, Ownable  {
    constructor() ERC20("PuntosRecomensasCoin", "PRC") {
        _mint(msg.sender,2*(10**6)*(10**18));
    }
}