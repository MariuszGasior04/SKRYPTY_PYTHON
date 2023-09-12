import ezdxf
from shutil import copyfile

if __name__ == '__main__':
    """parametry programu"""
    filename = r'C:\robo\ZASADNICZA\Pulawska\Map_zas_500.dxf'
    # filename = r'C:\robo\ZASADNICZA\boguchwala miasto.DXF'
    copydxf = r'C:\robo\ZASADNICZA\Pulawska\_test_copy_PULWSKA.DXF'

    layer_list = ['SUBK_L', 'SUBPP_L', 'SUOK_L', 'SUPK_L', 'SUPK_L', 'SUPP_L', 'SUPS_L', 'SUPS_T', 'SUTK_T', 'SUUK_E_T',
                  'SUUK_L', 'SUUK_T', 'SUUW_L', 'SUUW_T', 'SUUZ_L', 'SUUZ_T', 'SUXX_L', 'SUXX_T']

    copyfile(filename, copydxf)

    doc = ezdxf.readfile(copydxf)
    msp = doc.modelspace()
    delete_entities = []
    for entity in msp:
        print(entity.dxf.layer)
    #     if len(entity.dxf.layer) < 8:
    #         delete_entities.append(entity)
    #     else:
    #         check = [entity.dxf.layer[:6], entity.dxf.layer[:7], entity.dxf.layer[:8]]
    #         flag = False
    #         for f in check:
    #             if f in layer_list:
    #                 flag = True
    #         if not flag:
    #             delete_entities.append(entity)
    # for entity in msp:
    #     if entity.dxftype() == "LINE":
    #         msp.delete_entity(entity)
    #
    # for entity in delete_entities:
    #     # msp.unlink_entity(entity)
    #
    #     msp.delete_entity(entity)
    #
    # doc.save()
