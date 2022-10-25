// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.4;
import "./PuntosRecompensasCoin.sol";

contract PuntosFidelizacion{

    PuntosRecompensasCoin private puntos;

    // Direccion del creador de los puntos
    address public creador;

    constructor () {
        puntos = new PuntosRecompensasCoin();
        creador = msg.sender;
    }

    // Estructura de datos para almacenar a los clientes del programa
    struct Cliente {
        uint puntos_canjeados;
        string[] id_productos_comprados;
    }

    // Mapping para el registro de clientes
    mapping (address => Cliente) private clientes;

	// Balance de puntos de PuntosRecompensasCoin.
    function balanceDePuntos() public view returns (uint) {
        return puntos.balanceOf(address(this));
    }

    // Modificador que verifica que seas el creador del programa
    modifier soloCreador(address _direccion) {
        require(_direccion == creador, "No tienes permisos para ejecutar esta funcion.");
        _;
    }

    // Funcion que agrega un nuevo cliente al mapping de clientes
    function agregarCliente(address _direccion) public  {
        clientes[_direccion] = Cliente(0,new string[](0));
    }

    // Funcion que retorna un cliente del mapping de clientes
    function obtenerCliente(address _direccion) public view returns (Cliente memory) {
        return clientes[_direccion];
    }

    // Funcion que obtiene Puntos conseguidos en una tienda
    function canjearPuntos(uint _numPuntos,string memory _id_producto) public {
        // Obtenemos el numero de tokens disponibles
        uint Balance = balanceDePuntos();
        require(_numPuntos <= Balance, "No quedan puntos disponibles para comprar");
        // Se transfieren los puntos al cliente
        puntos.transfer(msg.sender, _numPuntos);
        // Registro de tokens comprados
        clientes[msg.sender].puntos_canjeados += _numPuntos;
        clientes[msg.sender].id_productos_comprados.push(_id_producto);
    }

    // Consulta saldo de tokens de un cliente.
    function obtenerPuntos() public view returns (uint){
        return puntos.balanceOf(msg.sender);
    }

}