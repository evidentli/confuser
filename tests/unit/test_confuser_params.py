from unittest import TestCase

from confuser.confuser_params import params,synthea

class TestConfuserParams(TestCase):

    def test_params_max_typos( self ):
        assert 'max_typos' in dir(params)

    def test_params_p_typo( self ):
        assert 'p_typo' in dir(params)
        assert params.p_typo >= 0
        assert params.p_typo <= 1

    def test_param_p_switch_table( self ):
        assert 'p_switch_table' in dir(params)
        assert params.p_switch_table >= 0
        assert params.p_switch_table <= 1

    def test_params_p_omit_row( self ):
        assert 'p_omit_row' in dir(params)
        assert params.p_omit_row >= 0
        assert params.p_omit_row <= 1

    def test_params_p_misplace_row( self ):
        assert 'p_misplace_row' in dir(params)
        assert params.p_misplace_row >= 0
        assert params.p_misplace_row <= 1

    def test_params_p_drop_value( self ):
        assert 'p_drop_value' in dir(params)
        assert params.p_drop_value >= 0
        assert params.p_drop_value <= 1

    def test_params_p_dup_row( self ):
        assert 'p_dup_row' in dir(params)
        assert params.p_dup_row >= 0
        assert params.p_dup_row <= 1

    def test_params_p_del_char( self ):
        assert 'p_del_char' in dir(params)
        assert params.p_del_char >= 0
        assert params.p_del_char <= 1

    def test_params_p_ins_char( self ):
        assert 'p_ins_char' in dir(params)
        assert params.p_ins_char >= 0
        assert params.p_ins_char <= 1

    def test_params_p_transp_char( self ):
        assert 'p_transp_char' in dir(params)
        assert params.p_transp_char >= 0
        assert params.p_transp_char <= 1

    def test_params_p_rep_char( self ):
        assert 'p_rep_char' in dir(params)
        assert params.p_rep_char >= 0
        assert params.p_rep_char <= 1

    def test_params_p_dup_char( self ):
        assert 'p_dup_char' in dir(params)
        assert params.p_dup_char >= 0
        assert params.p_dup_char <= 1

    def test_params_p_tog_case_char( self ):
        assert 'p_tog_case_char' in dir(params)
        assert params.p_tog_case_char >= 0
        assert params.p_tog_case_char <= 1

    def test_params_obscure_headers( self ):
        assert 'obscure_schema' in dir(params)

    def test_params_p_swap_dates( self ):
        assert 'p_swap_dates' in dir(params)
        assert params.p_swap_dates >= 0
        assert params.p_swap_dates <= 1

    def test_prarms_p_split_table( self ):
        assert 'p_split_table' in dir(params)
        assert params.p_split_table >= 0
        assert params.p_split_table <= 1

    def test_prarms_mult( self ):
        assert 'mult' in dir(params)
        assert params.mult >= 0
        assert params.mult <= 1

    """""" """""" """""" """""" """""" """"""

    def test_synthea_csv_files( self ):
        assert 'csv_files' in dir(synthea)
        assert len(synthea.csv_files) == 16

    def test_synthea_desc_header( self ):
        assert 'desc_header' in dir(synthea)

