from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Set, Optional, List

from ..util import Coord, VehicleTransfer
from ..vehicles import Vehicle
from ..lanes import IntersectionLane, ScheduledExit

if TYPE_CHECKING:
    from .tilings import Tile


@dataclass
class Reservation:
    """
    Vehicles waiting in a road lane to enter an intersection must successfully
    reserve timespace tiles in the intersection in order to pass through. The
    intersection's manager and tiling process reservation requests based on
    feasibility and priority to decide which reservations to accept.

    After a reservation is created, the only properties that are modified are
    the tiles (by adding new tiles used each timestep of the reservation test),
    the dependency property (if we see another vehicle in its sequence get
    added), and its_exit (when the reservation test progresses to the point
    where we know when the vehicle's rear section enters the intersection).

    Parameters
        vehicle: Vehicle
        res_pos: Coord
        tiles: Dict[int, Dict[Tile, float]]
            A dict with timesteps keyed to to the tiles used at that timestep
            and the proportion at which they're used.
            # TODO: (stochastic) The tiles themselves probably hold these
            #       probabilities. Are these necessary to save here?
        lane: IntersectionLane
        dependent_on: Set[Vehicle]
            The set of vehicles whose reservations this vehicle's reservation
            is dependent on, i.e., the vehicles preceding it in a sequenced
            reservation.
        dependency: Optional[Vehicle]
            The first vehicle dependent on this vehicle's reservation, i.e.,
            the vehicle immediately following this one in a sequenced
            reservation.
        its_exit: ScheduledExit
            The scheduled time and speed of the vehicle's exit from road into
            intersection. (Initialized as the scheduled exit of the front
            section of the vehicle as when the reservation is created that's
            the only information available. This is replaced by the test
            observed time of exit when that is found.)
            (Note: This is NOT the scheduled exit out of the intersection.)
    """
    vehicle: Vehicle
    res_pos: Coord
    tiles: Dict[int, Dict[Tile, float]]
    lane: IntersectionLane
    dependent_on: Set[Vehicle]
    dependency: Optional[Vehicle]
    its_exit: ScheduledExit

    def __hash__(self):
        return hash(vehicle)
