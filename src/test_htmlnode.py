from htmlnode import HTMLNode, LeafNode

def test_props_to_html():
    node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
    result = node.props_to_html()
    print(result)
    
def test_leaf_to_html_p():
    node = LeafNode("p", "Hello, world!")
    result = node.to_html()
    expected = "<p>Hello, world!</p>"
    assert result == expected, f"Expected '{expected}', got '{result}'"
    print("test_leaf_to_html_p passed!")

def test_leaf_to_html_a_with_props():
    node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    result = node.to_html()
    expected = '<a href="https://www.google.com">Click me!</a>'
    assert result == expected, f"Expected '{expected}', got '{result}'"
    print("test_leaf_to_html_a_with_props passed!")

def test_leaf_to_html_no_tag():
    node = LeafNode(None, "Just some text")
    result = node.to_html()
    expected = "Just some text"
    assert result == expected, f"Expected '{expected}', got '{result}'"
    print("test_leaf_to_html_no_tag passed!")

def test_leaf_to_html_no_value():
    try:
        node = LeafNode("p", None)
        node.to_html()
        assert False, "Expected ValueError was not raised"
    except ValueError:
        print("test_leaf_to_html_no_value passed!")

if __name__ == "__main__":
    test_props_to_html()
    test_leaf_to_html_p()
    test_leaf_to_html_a_with_props()
    test_leaf_to_html_no_tag()
    test_leaf_to_html_no_value()
