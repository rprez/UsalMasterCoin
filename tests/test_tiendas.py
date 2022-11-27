#!/usr/bin/python3
import brownie

#Modulo que prueba el contrato de las gestion de las tiendas.
INITIAL_SUPPLY = 2000000000000000000000000


def test_saldo_puntos(accounts, contratosTienda):
    puntosSaldo = contratosTienda.balanceSupply({'from': accounts[0]})

    assert puntosSaldo == INITIAL_SUPPLY

#Test donde se transfiere puntos a una tienda y la tienda verifica su saldo con la llamada al contrato.
def test_nueva_tienda(accounts, contratosTienda):
    contratosTienda.crearNuevaTienda(1,accounts[1],{'from':accounts[0]})
    contratosTienda.transferirPuntosTienda(10000000,accounts[1], {'from': accounts[0]})

    contratosTienda.crearNuevaTienda(2, accounts[2], {'from': accounts[0]})
    contratosTienda.transferirPuntosTienda(20000000, accounts[2], {'from': accounts[0]})

    saldo_tienda1 = contratosTienda.obtenerPuntos(accounts[1],{'from':accounts[1]})
    saldo_tienda2 = contratosTienda.obtenerPuntos(accounts[2],{'from':accounts[2]})

    assert saldo_tienda1 == 10000000
    assert saldo_tienda2 == 20000000

#Test que prueba agregar dos tiendas nuevas y comprobar el saldo de las dos con los puntos inicial.
def test_nuevas_tienda(accounts, contratosTienda):
    contratosTienda.crearNuevaTienda(1,accounts[1],{'from':accounts[0]})
    contratosTienda.transferirPuntosTienda(10000000,accounts[1], {'from': accounts[0]})

    saldo_tienda1 = contratosTienda.obtenerPuntos(accounts[1],{'from': accounts[1]})
    assert saldo_tienda1 == 10000000

    contratosTienda.crearNuevaTienda(2, accounts[2], {'from': accounts[0]})
    contratosTienda.transferirPuntosTienda(20000000, accounts[2], {'from': accounts[0]})

    saldo_tienda2 = contratosTienda.obtenerPuntos(accounts[2],{'from': accounts[2]})
    assert saldo_tienda2 == 20000000

    puntosSaldo = contratosTienda.balanceSupply({'from': accounts[0]})

    assert puntosSaldo == INITIAL_SUPPLY - saldo_tienda1 - saldo_tienda2

#Test que verifica la creacion de nuevos clientes, con 0 puntos y lista vacia de productos
def test_nuevo_cliente(accounts, contratosTienda):

    #Direcciones del owner y de la tienda
    owner_addr = accounts[0]
    tienda_addr = accounts[1]

    #Direcciones de los clientes
    cliente1_addr = accounts[2]
    cliente2_addr = accounts[3]


    contratosTienda.crearNuevaTienda(1, tienda_addr, {'from': owner_addr})

    contratosTienda.agregarCliente(1, cliente1_addr, {'from': tienda_addr})
    contratosTienda.agregarCliente(2, cliente2_addr, {'from': tienda_addr})

    cliente1 = contratosTienda.obtenerCliente(cliente1_addr, {'from': tienda_addr})
    cliente2 = contratosTienda.obtenerCliente(cliente2_addr, {'from': tienda_addr})

    assert cliente1 is not None
    assert cliente2 is not None

    assert cliente1['id_cliente'] == '1' and cliente1['puntos_recompensas'] == 0 and cliente1['id_productos_comprados'] == []
    assert cliente2['id_cliente'] == '2' and cliente2['puntos_recompensas'] == 0 and cliente2['id_productos_comprados'] == []


#Este test valida la función que llama la tienda para transferir puntos a un cliente.
#Se retira saldo de puntos de una tienda, se transfiere al cliente y se verifica
#saldo de puntos de la tienda y del cliente.
def test_compra_cliente(accounts,contratosTienda):

    # Direcciones del owner, de la tienda y el cliente
    owner_addr = accounts[0]
    tienda_addr = accounts[1]
    cliente_addr = accounts[2]

    #Creamos la tienda y le transferimos puntos.
    contratosTienda.crearNuevaTienda(1, tienda_addr, {'from': owner_addr})
    contratosTienda.transferirPuntosTienda(10000000, tienda_addr, {'from': owner_addr})
    saldo_tienda1 = contratosTienda.obtenerPuntos(accounts[1],{'from': accounts[1]})

    assert saldo_tienda1 == 10000000

    #Asociamos nuevo cliente a la tienda.
    contratosTienda.agregarCliente(1, cliente_addr, {'from': tienda_addr})
    #Cliente realiza una compra y la tienda llama al contrato para transferir puntos.
    contratosTienda.transferirPuntosCliente(10,"a34",cliente_addr,{'from': tienda_addr})

    #Verificamos que el cliente tenga los puntos obtenidos
    puntosCliente = contratosTienda.obtenerPuntos(cliente_addr, {'from': tienda_addr})

    assert puntosCliente == 10

    #Verificamos que cambió el saldo de la tienda y de los tokens.
    total_ptos_tienda = contratosTienda.obtenerPuntos(tienda_addr,{'from': tienda_addr})
    assert total_ptos_tienda == (10000000 - puntosCliente)

    puntosSaldo = contratosTienda.balanceSupply({'from': accounts[0]})
    assert puntosSaldo == INITIAL_SUPPLY - saldo_tienda1


def test_canje_cliente(accounts,contratosTienda):
    # Direcciones del owner, de la tienda y el cliente
    owner_addr = accounts[0]
    tienda_addr = accounts[1]
    cliente_addr = accounts[2]

    # Creamos la tienda y le transferimos puntos.
    contratosTienda.crearNuevaTienda(1, tienda_addr, {'from': owner_addr})
    contratosTienda.transferirPuntosTienda(10000000, tienda_addr, {'from': owner_addr})
    saldo_tienda1 = contratosTienda.obtenerPuntos(accounts[1], {'from': tienda_addr})

    assert saldo_tienda1 == 10000000

    # Asociamos nuevo cliente a la tienda.
    contratosTienda.agregarCliente(1, cliente_addr, {'from': tienda_addr})
    # Cliente realiza una compra y la tienda llama al contrato para transferir puntos.
    contratosTienda.transferirPuntosCliente(10, "a34", cliente_addr, {'from': tienda_addr})

    # Verificamos que el cliente tenga los puntos obtenidos
    puntosCliente = contratosTienda.obtenerPuntos(cliente_addr, {'from': tienda_addr})

    assert puntosCliente == 10

    # Verificamos que cambió el saldo de la tienda y de los tokens.
    total_ptos_tienda = contratosTienda.obtenerPuntos(tienda_addr, {'from': tienda_addr})
    assert total_ptos_tienda == (10000000 - puntosCliente)

    contratosTienda.canjearPuntosTienda(2,tienda_addr,{'from':cliente_addr})

    # Verificamos que cambió el saldo de la tienda y de los tokens.
    total_ptos_tienda = contratosTienda.obtenerPuntos(tienda_addr, {'from': tienda_addr})
    assert total_ptos_tienda == (10000000 - puntosCliente) + 2

    # Verificamos que el cliente canjeó los puntos obtenidos
    puntosCliente = contratosTienda.obtenerPuntos(cliente_addr, {'from': tienda_addr})

    assert puntosCliente == 10 - 2