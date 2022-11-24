#!/usr/bin/python3
import brownie

#Modulo que prueba el contrato de las gestion de las tiendas.
def test_saldo_puntos(accounts, contratosTienda):
    puntosSaldo = contratosTienda.balanceDePuntos()

    assert puntosSaldo == 2000000000000000000000000

#Test donde se transfiere puntos a una tienda y la tienda verifica su saldo con la llamada al contrato.
def test_nueva_tienda(accounts, contratosTienda):
    contratosTienda.crearNuevaTienda(1,accounts[1],{'from':accounts[0]})
    contratosTienda.transferirPuntosTienda(10000000,accounts[1], {'from': accounts[0]})

    contratosTienda.crearNuevaTienda(2, accounts[2], {'from': accounts[0]})
    contratosTienda.transferirPuntosTienda(20000000, accounts[2], {'from': accounts[0]})

    saldo_tienda1 = contratosTienda.saldoPuntosTienda(accounts[1],{'from':accounts[0]})
    saldo_tienda2 = contratosTienda.saldoPuntosTienda(accounts[2],{'from':accounts[0]})

    assert saldo_tienda1 == 10000000
    assert saldo_tienda2 == 20000000

#Test que prueba agregar dos tiendas nuevas y comprobar el saldo de las dos con los puntos inicial.
def test_nuevas_tienda(accounts, contratosTienda):
    contratosTienda.crearNuevaTienda(1,accounts[1],{'from':accounts[0]})
    contratosTienda.transferirPuntosTienda(10000000,accounts[1], {'from': accounts[0]})

    puntosSaldo = contratosTienda.balanceDePuntos()
    total_ptos_tienda = contratosTienda.balanceTiendaPuntos( {'from': accounts[1]})
    assert puntosSaldo == 2000000000000000000000000 - total_ptos_tienda

    contratosTienda.crearNuevaTienda(2, accounts[2], {'from': accounts[0]})
    contratosTienda.transferirPuntosTienda(20000000, accounts[2], {'from': accounts[0]})

    puntosSaldo = contratosTienda.balanceDePuntos()
    total_ptos_tienda2 = contratosTienda.balanceTiendaPuntos({'from': accounts[2]})
    assert puntosSaldo == 2000000000000000000000000 - total_ptos_tienda - total_ptos_tienda2

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