from __future__ import annotations

__author__ = 'github.com/arm61'

import numbers
from copy import deepcopy
from typing import Callable

import yaml
from easyCore import np
from easyCore.Objects.ObjectClasses import BaseObj
from easyCore.Objects.ObjectClasses import Parameter

from EasyReflectometry.sample import BaseAssembly
from EasyReflectometry.sample import Layer
from EasyReflectometry.sample import LayerCollection
from EasyReflectometry.sample import Sample

from .resolution_functions import constant_resolution_function

MODEL_DETAILS = {
    'scale': {
        'description': 'Scaling of the reflectomety profile',
        'url': 'https://github.com/reflectivity/edu_outreach/blob/master/refl_maths/paper.tex',
        'value': 1.0,
        'min': 0,
        'max': np.Inf,
        'fixed': True,
    },
    'background': {
        'description': 'Linear background to include in reflectometry data',
        'url': 'https://github.com/reflectivity/edu_outreach/blob/master/refl_maths/paper.tex',
        'value': 1e-8,
        'min': 0.0,
        'max': np.Inf,
        'fixed': True,
    },
    'resolution': {
        'value': 5.0,
    },
}


class Model(BaseObj):
    """Model is the class that represents the experiment.
    It is used to store the information about the experiment and to perform the calculations.
    """

    # Added in super().__init__
    name: str
    sample: Sample
    scale: Parameter
    background: Parameter

    def __init__(
        self,
        sample: Sample,
        scale: Parameter,
        background: Parameter,
        resolution_function: Callable[[np.array], float],
        name: str = 'EasyModel',
        interface=None,
    ):
        """Constructor.

        :param sample: The sample being modelled.
        :param scale: Scaling factor of profile.
        :param background: Linear background magnitude.
        :param name: Name of the model, defaults to 'EasyModel'.
        :param interface: Calculator interface, defaults to `None`.

        """
        super().__init__(
            name=name,
            sample=sample,
            scale=scale,
            background=background,
        )
        self.interface = interface
        if not callable(resolution_function):
            raise ValueError('Resolution function must be a callable.')
        self._resolution_function = resolution_function

    # Class methods for instance creation
    @classmethod
    def default(cls, interface=None) -> Model:
        """Default instance of the reflectometry experiment model.

        :param interface: Calculator interface, defaults to `None`.
        """
        sample = Sample.default()
        scale = Parameter('scale', **MODEL_DETAILS['scale'])
        background = Parameter('background', **MODEL_DETAILS['background'])
        resolution_function = constant_resolution_function(MODEL_DETAILS['resolution']['value'])

        return cls(
            sample=sample,
            scale=scale,
            background=background,
            resolution_function=resolution_function,
            interface=interface,
        )

    @classmethod
    def from_pars(
        cls,
        sample: Sample,
        scale: float,
        background: float,
        resolution_function: float | Callable[[np.array], float],
        name: str = 'EasyModel',
        interface=None,
    ) -> Model:
        """Instance of a reflectometry experiment model where the parameters are known.

        :param sample: The sample being modelled.
        :param scale: Scaling factor of profile.
        :param background: Linear background magnitude.
        :param name: Name of the layer, defaults to 'EasyModel'.
        :param interface: Calculator interface, defaults to `None`.
        """
        default_options = deepcopy(MODEL_DETAILS)
        del default_options['scale']['value']
        del default_options['background']['value']

        scale = Parameter('scale', scale, **default_options['scale'])
        background = Parameter('background', background, **default_options['background'])

        if isinstance(resolution_function, numbers.Number):
            resolution_function = constant_resolution_function(resolution_function)

        return cls(
            sample=sample,
            scale=scale,
            background=background,
            resolution_function=resolution_function,
            name=name,
            interface=interface,
        )

    def add_item(self, *assemblies: list[BaseAssembly]) -> None:
        """Add a layer or item to the model sample.

        :param assemblies: Assemblies to add to model sample.
        """
        for arg in assemblies:
            if issubclass(arg.__class__, BaseAssembly):
                self.sample.append(arg)
                if self.interface is not None:
                    self.interface().add_item_to_model(arg.uid, self.uid)
            else:
                raise ValueError(f'Object {arg} is not a valid type, must be a child of BaseAssembly.')

    def duplicate_item(self, idx: int) -> None:
        """Duplicate a given item or layer in a sample.

        :param idx: Index of the item or layer to duplicate
        """
        to_duplicate = self.sample[idx]
        duplicate_layers = []
        for i in to_duplicate.layers:
            duplicate_layers.append(
                Layer.from_pars(
                    material=i.material,
                    thickness=i.thickness.raw_value,
                    roughness=i.roughness.raw_value,
                    name=i.name + ' duplicate',
                )
            )
        duplicate = to_duplicate.__class__.from_pars(
            LayerCollection.from_pars(*duplicate_layers, name=to_duplicate.layers.name + ' duplicate'),
            name=to_duplicate.name + ' duplicate',
        )
        self.add_item(duplicate)

    def remove_item(self, idx: int) -> None:
        """Remove an item from the model.

        :param idx: Index of the item to remove.
        """
        if self.interface is not None:
            self.interface().remove_item_from_model(self.sample[idx].uid, self.uid)
        del self.sample[idx]

    def set_resolution_function(self, resolution_function: Callable[[np.array], float]) -> None:
        """Set the resolution function for the model.

        :param resolution_function: Resolution function to set.
        """
        self._resolution_function = resolution_function

    @property
    def uid(self) -> int:
        """Return a UID from the borg map."""
        return self._borg.map.convert_id_to_key(self)

    # Representation
    @property
    def _dict_repr(self) -> dict[str, dict[str, str]]:
        """A simplified dict representation."""
        if self._resolution_function.__qualname__.split('.')[0] == 'constant_resolution_function':
            resolution_value = self._resolution_function([0])[0]
            resolution = f'{resolution_value} %'
        else:
            resolution = 'function of Q'

        return {
            self.name: {
                'scale': self.scale.raw_value,
                'background': self.background.raw_value,
                'resolution': resolution,
                'sample': self.sample._dict_repr,
            }
        }

    def __repr__(self) -> str:
        """String representation of the layer."""
        return yaml.dump(self._dict_repr, sort_keys=False)

    def as_dict(self, skip: list = None) -> dict:
        """Produces a cleaned dict using a custom as_dict method to skip necessary things.
        The resulting dict matches the paramters in __init__

        :param skip: List of keys to skip, defaults to `None`.
        """
        if skip is None:
            skip = []
        this_dict = super().as_dict(skip=skip)
        this_dict['sample'] = self.sample.as_dict()
        return this_dict
