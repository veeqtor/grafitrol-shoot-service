"""ALl response Messages"""

ERROR_MSG = {
    'SYS_001': 'An error has occurred.',
    'SYS_002': 'Invalid field(s) provided.',
    'SYS_003': 'Invalid `date` format, should be in this format (YYYY-MM-DD).',
    'SYS_004': 'Should not be less than {}',
    'SYS_005': 'Should not be more than {}',
    'SYS_006': 'Invalid ID provided.',
    'SYS_007': 'Not found.',
    'SYS_008': 'Missing data for required field.',
    'CO_001': 'No coordinator available.',
    'RES_001': 'Cannot process reservation, slot not available',
    'RES_002': 'Cannot perform this action.',
    'RES_003': 'Cannot exceed shoot duration.',
}

SUCCESS_MSG = {
    'SYS_001': 'Successfully created.',
    'SYS_002': 'Successfully deleted.',
    'SYS_003': 'Successfully updated.',
}
