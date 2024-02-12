from __future__ import annotations

from ..elementals.layer_collection import LayerCollection
from ..elementals.layers.layer import Layer
from .base import BaseAssembly


class MultiLayer(BaseAssembly):
    """
    A :py:class:`MultiLayer` consists of a series of
    :py:class:`EasyReflectometry.sample.layer.Layer` or
    :py:class:`EasyReflectometry.sample.layers.Layers`.
    This :py:mod:`item` will arrange the layers as slabs, one on top of another,
    allowing the reflectometry to be determined from them.

    More information about the usage of this item is available in the
    `item library documentation`_

    .. _`item library documentation`: ./item_library.html#multilayer
    """

    def __init__(
        self,
        layers: LayerCollection | Layer | list[Layer],
        name: str = 'EasyMultiLayer',
        interface=None,
        type: str = 'Multi-layer',
    ):
        if isinstance(layers, Layer):
            layers = LayerCollection(layers, name=layers.name)
        elif isinstance(layers, list):
            layers = LayerCollection(*layers, name='/'.join([layer.name for layer in layers]))
        self.type = type
        super().__init__(name, layers=layers, interface=interface)

    # Class constructors
    @classmethod
    def default(cls, interface=None) -> MultiLayer:
        """
        Default constructor for a multi-layer item.

        :return: MultiLayer container
        :rtype: MultiLayer
        """
        layers = LayerCollection.default()
        return cls(layers, interface=interface)

    @classmethod
    def from_pars(cls, layers: LayerCollection, name: str = 'EasyMultiLayer', interface=None) -> MultiLayer:
        """
        Constructor of a multi-layer item where the parameters are known.

        :param layers: The layers in the multi-layer
        :type layers: EasyReflectometry.layers.Layers
        :return: MultiLayer container
        :rtype: MultiLayer
        """
        return cls(layers=layers, name=name, interface=interface)

    def add_layer(self, *layers):
        """
        Add a layer to the item.

        :param *layers: Layers to add to item
        :type layers: Layer
        """
        for arg in layers:
            if issubclass(arg.__class__, Layer):
                self.layers.append(arg)
                if self.interface is not None:
                    self.interface().add_layer_to_item(arg.uid, self.uid)

    def duplicate_layer(self, idx):
        """
        Duplicate a given layer.

        :param idx: index of layer to duplicate
        :type idx: int
        """
        to_duplicate = self.layers[idx]
        duplicate_layer = Layer.from_pars(
            material=to_duplicate.material,
            thickness=to_duplicate.thickness.raw_value,
            roughness=to_duplicate.roughness.raw_value,
            name=to_duplicate.name + ' duplicate',
        )
        self.add_layer(duplicate_layer)

    def remove_layer(self, idx):
        """
        Remove a layer from the item.

        :param idx: index of layer to remove
        :type idx: int
        """
        if self.interface is not None:
            self.interface().remove_layer_from_item(self.layers[idx].uid, self.uid)
        del self.layers[idx]

    # Representation
    @property
    def _dict_repr(self) -> dict:
        """
        A simplified dict representation.

        :return: Simple dictionary
        """
        if len(self.layers) == 1:
            return self.layers[0]._dict_repr
        return {self.name: self.layers._dict_repr}