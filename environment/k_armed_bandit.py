"""
This module contains the one-armed bandit and k-armed bandit environments.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class OneArmedBandit:
    """
    A one-armed bandit with a single action and a single state.
    """

    def __init__(self, mean, std):
        """
        Initialize the one-armed bandit.

        Args:
            mean (float): The mean reward.
            std (float): The standard deviation of the reward.
        """
        self.mean = mean
        self.std = std

    def get_reward(self):
        """
        Get a reward from the one-armed bandit.

        Returns:
            float: The reward.
        """
        return np.random.normal(self.mean, self.std)

    def __str__(self):
        return f"OneArmedBandit(mean={self.mean}, std={self.std})"

    def __repr__(self):
        return str(self)


class KArmedBandit:
    """
    A k-armed bandit with k actions and a single state.

    Initialised with constant, k, which instantiates k one-armed bandits with mean rewards drawn from a normal dist.
    """

    def __init__(self, k, k_mean=0, k_std=1, bandit_std=1, random_seed=None):
        self.k = k
        self.k_mean = k_mean
        self.k_std = k_std
        self.bandit_std = bandit_std
        self.random_seed = random_seed
        self.bandits = self._init_bandits()

    def _init_bandits(self):
        """
        Initialise the bandits.

        Returns:
            list: A list of one-armed bandits.
        """
        if self.random_seed is not None:
            np.random.seed(self.random_seed)
        k_means = np.random.normal(self.k_mean, self.k_std, self.k)
        bandits = [OneArmedBandit(mean, self.bandit_std) for mean in k_means]
        return bandits

    def get_reward(self, action):
        """
        Get a reward from the k-armed bandit.

        Args:
            action (int): The action to take.

        Returns:
            float: The reward.
        """
        return self.bandits[action].get_reward()

    def __str__(self):
        return f"KArmedBandit(k={self.k}, k_mean={self.k_mean}, k_std={self.k_std}, bandit_std={self.bandit_std})"

    def __repr__(self):
        return str(self)

    def show(self, title=None):
        """
        Violin plot of the distributions of the bandits.
        """
        # Add a horizontal dashed line in the background at y=0. The violin plots will be plotted on top of this.
        plt.axhline(y=0, color="black", linestyle="--", alpha=0.25)

        # Sample 250 points from each of the bandits, and plot the distributions of these points
        data = []
        for bandit in self.bandits:
            samples = [bandit.get_reward() for _ in range(250)]
            data.append(samples)
        sns.violinplot(data=data)

        if title is not None:
            plt.title(title)

        plt.show()


class KArmedTestbed:
    """
    A testbed for k-armed bandit algorithms: contains a set of `num_runs` k-armed bandits, to test bandit algorithms
    on a
    varying set of runs.

    See pp28 of Sutton and Barto for details (here, `num_runs` is 2000)

    Boolean parameter `with_seed` determines whether the k-armed bandits are instantiated with a random seed or not,
    for reproducibility. If true, then select random seeds deterministically from range(0, num_runs).
    """

    def __init__(self, num_runs, k, k_mean=0, k_std=1, bandit_std=1, with_seed=False):
        self.num_runs = num_runs
        self.k = k
        self.k_mean = k_mean
        self.k_std = k_std
        self.bandit_std = bandit_std
        self.with_seed = with_seed
        self.bandits = self._init_bandits()

    def _init_bandits(self):
        """
        Initialise the bandits.

        Returns:
            list: A list of k-armed bandits.
        """
        if self.with_seed:
            bandits = [KArmedBandit(self.k, self.k_mean, self.k_std, self.bandit_std, random_seed=i) for i in
                       range(self.num_runs)]
        else:
            bandits = [KArmedBandit(self.k, self.k_mean, self.k_std, self.bandit_std) for _ in range(self.num_runs)]
        return bandits

    def get_k_armed_bandit(self, run):
        """
        Get the k-armed bandit for a given run.

        Args:
            run (int): The run.

        Returns:
            KArmedBandit: The k-armed bandit for the given run.
        """
        return self.bandits[run]

    def show(self):
        """
        For each run, runs KArmedBandit.show(). Adds a title to each plot with the run number.
        """
        for i, bandit in enumerate(self.bandits):
            title = f"Run {i}"
            bandit.show(title=title)



def main():
    """
    Test the k-armed bandit environment.
    """
    k_armed_testbed = KArmedTestbed(num_runs=3, k=10, k_mean=0, k_std=1, bandit_std=1, with_seed=True)
    k_armed_testbed.show()


if __name__ == "__main__":
    main()
