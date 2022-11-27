// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.4;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract PuntosRecompensasCoin is ERC20, Ownable  {
    constructor() ERC20("PuntosRecomensasCoin", "PRC") {
        _mint(msg.sender,2*(10**6)*(10**18));
    }

    /***********************/
    /* Gestion de tiendas **/
    /***********************/

    // Estructura de datos para almacenar a las tiendas del programa
    struct Tienda {
        string id_tienda;
        uint puntos_comprados;
    }

    // Mapping para el registro de tiendas al programa.
    mapping (address => Tienda) internal tiendas;

    function crearNuevaTienda(string memory _id_tienda, address _address_tienda) public onlyOwner {
        tiendas[_address_tienda] = Tienda(_id_tienda,0);
    }

    // Saldo de puntos de todo el programa disponible
    function balanceSupply() public onlyOwner view returns (uint) {
        return balanceOf(owner());
    }

    // Consulta saldo de tokens de un cliente.
    function obtenerPuntos(address _direccion) public verificarTienda view returns (uint){
        return balanceOf(_direccion);
    }

    // Funcion que transfiere puntos a la tienda. Solamente puede ser llamada por el owner
    // Primero verifica que saldo del supply de puntos y luego hace el registro en el mapping de tiendas
    function transferirPuntosTienda(uint _numPuntos, address address_tienda) public onlyOwner {
        uint supply_balance = balanceSupply();
        require(_numPuntos <= supply_balance, "No quedan puntos disponibles para transferir");

        transfer(address_tienda, _numPuntos);
        tiendas[address_tienda].puntos_comprados += _numPuntos;
    }


    /***********************/
    /* Gestion de clientes **/
    /***********************/

    // Estructura de datos para almacenar a los clientes del programa
    struct Cliente {
        string id_cliente;
        uint puntos_recompensas;
        string[] id_productos_comprados;
    }

    // Mapping para el registro de clientes por tienda.
    // Este mapping esta referencia por la dirección de la tienda y los clientes que tiene asociado.
    mapping(address => mapping (address => Cliente)) private clientes;

    // Modificador que verifica que la tienda exista en el programa
    modifier verificarTienda() {
        require(tiendas[msg.sender].puntos_comprados > 0, "No tienes permisos para ejecutar esta funcion.");
        _;
    }

    // Modificador que verifica que el cliente pertenezca a la tienda
    modifier verificarClienteTienda(address addres_tienda) {
        require(clientes[addres_tienda][msg.sender].puntos_recompensas > 0, "Debes ser cliente de la tienda para canjear puntos.");
        _;
    }

    // Funcion que agrega un nuevo cliente al mapping de clientes
    function agregarCliente(string memory _id_cliente, address _address_cliente) public  {
        clientes[msg.sender][_address_cliente] = Cliente(_id_cliente,0,new string[](0));
    }

    // Funcion que retorna un cliente del mapping de clientes
    function obtenerCliente(address _direccion) public view returns (Cliente memory) {
        return clientes[msg.sender][_direccion];
    }

    // Funcion que envia Puntos conseguidos en la tienda a un cliente.
    // El verificadorTienda verifica que el que llame a la función sea la tienda misma.
    // Verifica que la tienda tenga puntos antes de transferir los puntos al cliente.
    // Al final se registra los tokens transferido al cliente y del producto comprado.
    function transferirPuntosCliente(uint _numPuntos,string memory _id_producto,address _direccion_cliente) public verificarTienda {
        uint saldo_tienda = balanceOf(msg.sender);
        require(_numPuntos <= saldo_tienda, "No quedan puntos disponibles para transferir al cliente");

        transfer(_direccion_cliente, _numPuntos);

        clientes[msg.sender][_direccion_cliente].puntos_recompensas += _numPuntos;
        clientes[msg.sender][_direccion_cliente].id_productos_comprados.push(_id_producto);
    }

    // Funcion que invoca un cliente cuando canjea puntos de la tienda para comprar otro producto
    function canjearPuntosTienda(uint _numPuntos,address address_tienda) public verificarClienteTienda(address_tienda) {
        uint saldo_cliente = balanceOf(msg.sender);
        require(_numPuntos <= saldo_cliente, "No tiene suficientes puntos disponibles para canjear en la tienda");

        transfer(address_tienda,_numPuntos);
        clientes[address_tienda][msg.sender].puntos_recompensas -= _numPuntos;
    }
}