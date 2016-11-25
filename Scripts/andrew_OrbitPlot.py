import math
import rebound

def OrbitPlot(sim, figsize=(5,5), lim=None, Narc=100, unitlabel=None, color=False, periastron=False, trails=False, lw=1.):
        """
        Convenience function for plotting instantaneous orbits.

        Parameters
        ----------
        figsize         : tuple of float, optional
            Tuple defining the figure size (default: (5,5))
        lim             : float, optional           
            Limit for axes (default: None = automatically determined)
        unitlabel       : str, optional          
            String describing the units, shown on axis labels (default: None)
        color           : bool, optional            
            Enable color (default: False)
        periastron  : bool, optional            
            Draw a marker at periastron (default: False)
        trails          : bool, optional            
            Draw trails instead of solid lines (default: False)
        lw              : float, optional           
            Linewidth (default: 1.)

        Returns
        -------
        fig
            A matplotlib figure

        Examples
        --------
        The following example illustrates a typical use case.

        >>> sim = rebound.Simulation()
        >>> sim.add(m=1)
        >>> sim.add(a=1)
        >>> fig = rebound.OrbitPlot(sim)
        >>> fig.savefig("image.png") # save figure to file
        >>> fig.show() # show figure on screen

        """
        try:
            import matplotlib.pyplot as plt
            import matplotlib.cm as cm
            import matplotlib.colors as colors
            import numpy as np
        except:
            print("Error importing matplotlib and/or numpy. Plotting functions not available\n")
            return None
        norm = colors.Normalize(vmin=0, vmax=4)
        scale = cm.ScalarMappable(norm=norm, cmap="jet")
        fig, ax = plt.subplots(1, 1, figsize=figsize)
        orbits = sim.calculate_orbits()
        particles = sim.particles
        x = [p.x for p in particles]
        y = [p.y for p in particles]
        if lim is None:
            lim = 0.
            for o in orbits:
                if o.a>0.:
                    r = (1.+o.e)*o.a
                else:
                    r = o.d
                if r>lim:
                    lim = r
        ax.set_xlim([-lim,lim])
        ax.set_ylim([-lim,lim])

        if unitlabel is not None:
            unitlabel = " " + unitlabel
        else:
            unitlabel = ""
        #ax.set_xlabel("x"+unitlabel)
        #ax.set_ylabel("y"+unitlabel)
        ax.get_xaxis().set_ticks([])
        ax.get_yaxis().set_ticks([])
        ax.scatter(particles[0].x,particles[0].y, marker="*", s=35*lw, facecolor="black", edgecolor=None, zorder=3)
        for i, o in enumerate(orbits):
            if o.a < 300000:
                color = "green"
            elif o.a < 400000:
                color = "red"
            else:
                color = "blue"
            primary = sim.calculate_com(i+1)
            pp = rebound.Particle(a=o.a, f=o.f, inc=o.inc, omega=o.omega, Omega=o.Omega, e=o.e, m=particles[i+1].m, primary=primary, simulation=sim)
            #ax.scatter(pp.x, pp.y, s=25*lw, facecolor="black", edgecolor=None, zorder=3)
            if o.a>0.: # bound orbit
                phase = np.linspace(0,2.*np.pi,Narc)
                for ph in phase:
                    newp = rebound.Particle(a=o.a, f=o.f+ph, inc=o.inc, omega=o.omega, Omega=o.Omega, e=o.e, m=particles[i+1].m, primary=primary, simulation=sim)
                    #ax.plot([pp.x, newp.x], [pp.y, newp.y], color=color, zorder=2, lw=lw)
                    ax.plot([pp.x, newp.x], [pp.y, newp.y], color=scale.to_rgba(o.a), zorder=2, lw=lw)
                    pp = newp
            
            if periastron:
                newp = Particle(a=o.a, f=0., inc=o.inc, omega=o.omega, Omega=o.Omega, e=o.e, m=particles[i+1].m, primary=primary, simulation=sim)
                ax.plot([primary.x, newp.x], [primary.y, newp.y], linestyle="dotted", c=colori, zorder=1, lw=lw)
                ax.scatter([newp.x],[newp.y], marker="o", s=5.*lw, facecolor="none", edgecolor=colori, zorder=1)

        return fig
