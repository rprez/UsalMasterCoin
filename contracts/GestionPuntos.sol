// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.4;
import "./PuntosRecompensasCoin.sol";

//Contrato encargado de gestionar los puntos de fidelizacion para las diferentes tiendas
contract PuntosFidelizacion is Ownable {

    PuntosRecompensasCoin internal puntos;

    // Direccion del creador de los puntos
    address public administrador;

    constructor () {
        puntos = new PuntosRecompensasCoin();
        administrador = msg.sender;
    }

    // Estructura de datos para almacenar a las tiendas del programa
    struct Tienda {
        string id_tienda;
        uint puntos_comprados;
    }

    // Mapping para el registro de tiendas al programa.
    mapping (address => Tienda) internal tiendas;


    // Balance de puntos de PuntosRecompensasCoin.
    function balanceDePuntos() public virtual view returns (uint) {
        return puntos.balanceOf(address(this));
    }

    // Saldo de puntos de una tienda dada una direccion. 
    function saldoPuntosTienda(address _direccion) public onlyOwner view returns (uint) {
        return puntos.balanceOf(_direccion);
    }

    function crearNuevaTienda(string memory _id_tienda, address _address_tienda) public onlyOwner {
        tiendas[_address_tienda] = Tienda(_id_tienda,0);
    }

    function transferirPuntosTienda(uint _numPuntos, address address_tienda) public onlyOwner {
        // Obtenemos el numero de tokens disponibles
        uint Balance = balanceDePuntos();
        require(_numPuntos <= Balance, "No quedan puntos disponibles para transferir");
        // Se transfiere el saldo de puntos a la tienda.
        puntos.transfer(address_tienda, _numPuntos);
        // Registro de tokens comprados
        tiendas[address_tienda].puntos_comprados += _numPuntos;
    }

}