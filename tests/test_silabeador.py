from core.silabeador import separar_silabas_palabra


def test_separa_vocales_simples():
    assert separar_silabas_palabra("casa") == ["ca", "sa"]
    assert separar_silabas_palabra("camino") == ["ca", "mi", "no"]


def test_respeta_grupos_consonanticos_frecuentes():
    assert separar_silabas_palabra("plato") == ["pla", "to"]
    assert separar_silabas_palabra("clase") == ["cla", "se"]


def test_mantiene_diptongos_basicos():
    assert separar_silabas_palabra("cielo") == ["cie", "lo"]
    assert separar_silabas_palabra("causa") == ["cau", "sa"]


def test_separa_hiatos_por_tilde():
    assert separar_silabas_palabra("país") == ["pa", "ís"]
    assert separar_silabas_palabra("raíz") == ["ra", "íz"]


def test_palabra_vacia_devuelve_lista_vacia():
    assert separar_silabas_palabra("") == []


def test_casos_adicionales_de_silabeo():
    assert separar_silabas_palabra("mesa") == ["me", "sa"]
    assert separar_silabas_palabra("libro") == ["li", "bro"]
    assert separar_silabas_palabra("brazo") == ["bra", "zo"]
    assert separar_silabas_palabra("triste") == ["tris", "te"]
    assert separar_silabas_palabra("alto") == ["al", "to"]
    assert separar_silabas_palabra("cantar") == ["can", "tar"]
    assert separar_silabas_palabra("poeta") == ["po", "e", "ta"]
    assert separar_silabas_palabra("teatro") == ["te", "a", "tro"]
    assert separar_silabas_palabra("aire") == ["ai", "re"]
    assert separar_silabas_palabra("bueno") == ["bue", "no"]
    assert separar_silabas_palabra("ciudad") == ["ciu", "dad"]
