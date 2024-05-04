from files import md_file


def test_extract_photo_entry_id():
    hatena_id = 'SYM_simu'
    content = """
    文章1
    
    [f:id:SYM_simu:20230101154129p:image]
    
    文章2
    
    [f:id:SYM_simu:20230101154130p:image]
    
    文章3
    
    [f:id:SYM_simu:20230101154131p:image]
    
    文章4
    """

    ids = md_file.extract_photo_entry_id(hatena_id, content)
    assert len(ids) == 3
    assert ids[0] == '20230101154129'
    assert ids[1] == '20230101154130'
    assert ids[2] == '20230101154131'
