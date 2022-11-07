// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.4;
import "./GestionPuntos.sol";

contract ContratosTienda is PuntosFidelizacion {

   // Estructura de datos para almacenar a los clientes del programa
    struct Cliente {
        uint puntos_recompensas;
        string[] id_productos_comprados;
    }

    // Balance de puntos de PuntosRecompensasCoin de la tienda.
    function balanceDePuntos() public override view returns(uint) {
        return puntos.balanceOf(msg.sender);
    }

    // Mapping para el registro de clientes por tienda.
    // Este mapping esta referencia por la dirección de la tienda y los clientes que tiene asociado.
    mapping(address => mapping (address => Cliente)) private clientes;

    // Modificador que verifica que la tienda exista en el programa
    modifier verificarTienda() {
        require(tiendas[msg.sender].saldo_puntos >= 0, "No tienes permisos para ejecutar esta funcion.");
        _;
    }

    // Funcion que agrega un nuevo cliente al mapping de clientes
    function agregarCliente(address _direccion) public verificarTienda {
        clientes[msg.sender][_direccion] = Cliente(0,new string[](0));
    }

    // Funcion que retorna un cliente del mapping de clientes
    function obtenerCliente(address _direccion) public verificarTienda view returns (Cliente memory) {
        return clientes[msg.sender][_direccion];
    }

    // Funcion que obtiene los Puntos conseguidos en la tienda que invoca el contrato 
    function canjearPuntos(uint _numPuntos,string memory _id_producto) public verificarTienda {
        // Obtenemos el numero de tokens disponibles en la tienda.
        uint Balance = balanceDePuntos();
        require(_numPuntos <= Balance, "No quedan puntos disponibles para comprar");
        // Se transfieren los puntos al cliente
        puntos.transfer(msg.sender, _numPuntos);
        // Registro de tokens comprados
        clientes[msg.sender][msg.sender].puntos_recompensas += _numPuntos;
        clientes[msg.sender][msg.sender].id_productos_comprados.push(_id_producto);
    }

    // Consulta saldo de tokens de un cliente.
    function obtenerPuntosCliente(address _direccion) public verificarTienda view returns (uint){
        return puntos.balanceOf(_direccion);
    }

}