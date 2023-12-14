import pytest
from xml.etree.ElementTree import Element, ElementTree
from project import AbletonLOM, clean_description_for_X_Mind  # replace 'your_module' with the actual module name


def main():
    test_parse_path()
    test_get_listener_name()
    test_compare_listener_path()
    test_clean_description()


def test_parse_path():
    lom = AbletonLOM()
    result = lom.parse_path('Live.Tracks.add_mute_listener()')
    assert result == ['Live', 'Tracks', 'add_mute_listener()']


def test_get_listener_name():
    lom = AbletonLOM()
    result = lom.get_listener_name('add_solo_listener()')
    assert result == 'solo'
    result = lom.get_listener_name('solo_has_listener()')
    assert result == 'solo'
    result = lom.get_listener_name('any_other_method()')
    assert result == None


def test_compare_listener_path():
    lom = AbletonLOM()
    result = lom.compare_listener_path('add_mute_listener()', 'remove_mute_listener()')
    assert result == True


def test_clean_description():
    full_path = 'Live.WavetableDevice.WavetableDevice.View.is_collapsed_has_listener()'
    description = ('is_collapsed_has_listener( (View)arg1, (object)arg2) -&amp;gt; bool : Returns true, if the given listener function or '
                   'method is connected to the property "is_collapsed". C++ signature :  bool is_collapsed_has_listener(TPyViewData&amp;lt;ADevice&amp;gt;,'
                   'boost::python::api::object)')
    result = clean_description_for_X_Mind(description, full_path)
    assert result == ('full path:&#10;Live.WavetableDevice.WavetableDevice.View.is_collapsed_has_listener() &#10; &#10; is_collapsed_has_listener( '
                      '(View)arg1, (object)arg2) -&amp;gt; bool : Returns true, if the given listener function or method is connected to the property '
                      '&quot;is_collapsed&quot;.  &#10;&#10;C++ signature:  bool is_collapsed_has_listener'
                      '(TPyViewData&amp;lt;ADevice&amp;gt;,boost::python::api::object)')


if __name__ == "__main__":
    main()


