import pytest

def test_import_app_package():
    """Happy path: the app package imports successfully and is recognized as a package."""
    import app
    assert app is not None
    assert hasattr(app, '__path__'), "app should be a package (has __path__)"


def test_app_package_has_correct_name():
    """Edge case: the package has the expected __name__."""
    import app
    assert app.__name__ == 'app'


def test_app_package_contains_only_dunder_attributes():
    """Edge case: the empty package has no custom attributes beyond standard dunders."""
    import app
    standard_attrs = dir(type('', (), {}))  # attributes of a plain object
    non_dunders = [
        attr for attr in dir(app)
        if not (attr.startswith('__') and attr.endswith('__'))
    ]
    assert len(non_dunders) == 0, f"Unexpected non-dunder attributes: {non_dunders}"


def test_import_from_app_nonexistent_raises_import_error():
    """Error path: importing a name that does not exist in the app package raises ImportError."""
    with pytest.raises(ImportError) as exc_info:
        from app import nonexistent  # noqa: F401
    # Ensure the attribute name appears in the error message (common behaviour)
    assert "nonexistent" in str(exc_info.value) or "nonexistent" in str(exc_info.value).lower()