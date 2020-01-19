====
What
====
This is meant to be a menu driver for crashing hashes.

Examples
========

::

    # Manually add a hash if not specified on command line
    hashcrack > add hash 2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824
    # Be sure to set the type
    hashcrack > set hashtype SHA2-256
    # Optional -- tell hashcrack to use cpu if gpu is causing issues
    hashcrack > set device cpu
    # Crack it
    hashcrack > crack
    # If it's already cracked, show it
    hashcrack > show

    # Set your own wordlist (uses rockyou by default)
    hashcrack > set wordlist <path_to_wordlist>

Cracking WPA2
=============

``hashcrack`` will attempt to determine the correct settings and extract the
needed hashes for you. One example of this currently is pcaps. With hashcrack,
it's as simple as::

    $ hashcrack ./my.pcap
       ▄█    █▄       ▄████████    ▄████████    ▄█    █▄     ▄████████    ▄████████    ▄████████  ▄████████    ▄█   ▄█▄
      ███    ███     ███    ███   ███    ███   ███    ███   ███    ███   ███    ███   ███    ███ ███    ███   ███ ▄███▀
      ███    ███     ███    ███   ███    █▀    ███    ███   ███    █▀    ███    ███   ███    ███ ███    █▀    ███▐██▀
     ▄███▄▄▄▄███▄▄   ███    ███   ███         ▄███▄▄▄▄███▄▄ ███         ▄███▄▄▄▄██▀   ███    ███ ███         ▄█████▀
    ▀▀███▀▀▀▀███▀  ▀███████████ ▀███████████ ▀▀███▀▀▀▀███▀  ███        ▀▀███▀▀▀▀▀   ▀███████████ ███        ▀▀█████▄
      ███    ███     ███    ███          ███   ███    ███   ███    █▄  ▀███████████   ███    ███ ███    █▄    ███▐██▄
      ███    ███     ███    ███    ▄█    ███   ███    ███   ███    ███   ███    ███   ███    ███ ███    ███   ███ ▀███▄
      ███    █▀      ███    █▀   ▄████████▀    ███    █▀    ████████▀    ███    ███   ███    █▀  ████████▀    ███   ▀█▀
    Version 0.4 (https://github.com/bannsec/hashcrack)
    Powered by: Hashcat (hashcat.net)

    hashcrack > crack

.. note::

    You may have to adjust the `hashtype`, though the default will work for
    most PSK setups.
