BeagleBone Power Supply
=======
Draft

I want to make a cluster of [BeagleBones](http://beagleboard.org/bone),
so I'm pondering how to power them. It takes DC power from a plug with
the following specifications, taken from the
[recommended peripherals](http://beagleboard.org/peripheral#5V) page.

> The power adapter needs to provide 5V over a 5.5mm outer diameter
> and 2.1mm inner diameter barrel connector. A barrel connector length
> of 9.5mm is more than sufficient.
> The currently recommended supply current is at least 1.2A (or 6W),
>  but at least 2A (or 10W) is recommended if you are going to connect
> up anything over the USB. The actual power consumption will vary
> greatly with changes on the USB load.

BeagleBoard [recommendeds](http://beagleboard.org/peripheral#5V)
accomplishing this with a Digi-Key-supplied PHIHONG USA PSC12R-050.

I could just use a bunch of the recommended power supplies, similar to what
[Matt at Liquidware did](http://antipastohw.blogspot.com/2010/09/how-to-make-beagleboard-elastic-r.html),
but that seems messy and expensive.

I could just [use a standard PC power supply](http://www.instructables.com/id/Power-Supply-For-Arduino-power-and-breadboard/),
but that would be heavy and quite inefficient.

Powering the BeagleBones over [USB might not work](http://beagleboard.org/support/faq).

> The USB specification requires devices to power up under 100mA (~500mW)
> and the USB hub circuit on the BeagleBoard-xM may consume around 100mA
> itself. Modification is required to the kernel to avoid powering up this
> section of the board until sufficient current is confirmed by the software.
> In practice, most host machines will provide sufficient power, despite
> this violation of the specification. You should consider your power
> requirements before attempting to utilize USB to power your BeagleBoard
> or BeagleBoard-xM.

If it does, it would substantially increase power consumption; Revision 0.0 of the 
[BeagleBone Rev A5 System Reference Manual](http://beagleboard.org/static/BONESRM_latest.pdf)
(February 2, 2012) analyzes the "power consumption of the board in ...
various scenarious" in this table.

![Table of power usage indicating that plugging in the only USB cable
  uses about three-halves the power of plugging in only the DC cable
](beaglebone-power/beaglebone-power-consumption.png)

<!-- The table in LaTeX format
MODE                  & USB &  DC & DC+USB \\
Reset                 & 180 &  60 &    190 \\
UBoot                 & 363 & 230 &    340 \\
Kernel Booting (Peak) & 502 & 350 &    470 \\
Kernel Idling         & 305 & 170 &    290 \\
-->
