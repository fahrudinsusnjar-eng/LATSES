from lat_ces.core.dimensions import FORCE, LENGTH, MASS, TIME, VELOCITY, Dimension


def test_dimension_algebra():
    calculated_velocity = LENGTH / TIME
    assert calculated_velocity == VELOCITY

    mass_dim = Dimension(M=1)
    acc_dim = Dimension(L=1, T=-2)
    calculated_force = mass_dim * acc_dim
    assert calculated_force == FORCE

    assert MASS == Dimension(M=1)
