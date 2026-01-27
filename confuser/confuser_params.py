
class params_class:
    #the probability that a string will have typos
    p_typo = 0.3

    #maximum number of typos a string can have
    max_typos = 10

    #probability of breaking a table up after each row
    # a 0.00001 chance of breaking the table before this row (10 in 100000) means ~10,000 rows per table 
    # a 0.0005 chance (500 in 100000) means ~200 rows per table 
    p_switch_table = 0.00015

    #probability that a whole row is omitted
    p_omit_row = 0.1

    #probability that a whole row is placed in the wrong table
    p_misplace_row = 0.1

    #probability that a value will be replaced with NULL
    p_drop_value = 0.25

    #probability that a row is duplicated
    p_dup_row = 0.05

    #probability of deleting a character when confusing a string
    p_del_char = 0.2

    #probability of inserting a character when confusing a string
    p_ins_char = 0.15

    #probability of replacing a character with a random one when confusing a string
    p_transp_char = 0.15

    #probability of transposing two characters when confusing a string
    p_rep_char = 0.2

    #probability of toggling the case of a character when confusing a string
    p_tog_case_char = 0.15

    #probability of duplicating a charcter when confusing a string
    p_dup_char = 0.15

    #whether to obscure the schema (i.e. table and column names)
    obscure_schema = True

    #the probability that two dates on the same row will be swapped
    p_swap_dates = 0.001

    #the probability that a a table will be split in 2 vertically
    p_split_table = 0.01

    mult = 1.0

param_description = {
    'p_typo':'the probability that a string will have typos',
    'max_typos':'maximum number of typos a string can have',
    'p_switch_table':'probability of breaking a table up after each row. e.g. 0.00001 (1 in 10,000) means ~10,000 rows per table, 0.0005 (5 in 1,000) means ~200 rows per table ',
    'p_omit_row':'probability that a whole row is omitted',
    'p_misplace_row':'probability that a whole row is placed in the wrong table',
    'p_drop_value':'probability that a value will be replaced with NULL',
    'p_dup_row':'probability that a row is duplicated',
    'p_del_char':'probability of deleting a character when confusing a string',
    'p_ins_char':'probability of inserting a character when confusing a string',
    'p_rep_char':'probability of replacing a character with a random one when confusing a string',
    'p_transp_char':'probability of transposing two characters when confusing a string',
    'p_tog_case_char':'probability of toggling the case of a character when confusing a string',
    'p_dup_char':'probability of duplicating a charcter when confusing a string',
    'obscure_schema':'whether to obscure the schema (i.e. table and column names)',
    'p_swap_dates':'the probability that two dates on the same row will be swapped',
    'p_split_table':'the probability that a a table will be split in 2 vertically',
    'mult':'a number between 0 and 1 (inclusive) that will multiply all probability parameter (i.e. those that start with p_)'
    }

class synthea_class:
    csv_files = ( 'allergies.csv', 'careplans.csv', 'conditions.csv', 'devices.csv', 'encounters.csv', 'imaging_studies.csv', 
        'immunizations.csv', 'medications.csv', 'observations.csv', 'organizations.csv', 'patients.csv', 'payers.csv', 
        'payer_transitions.csv', 'procedures.csv', 'providers.csv', 'supplies.csv' )

    desc_header = 'DESCRIPTION'

synthea = synthea_class()
params = params_class()
