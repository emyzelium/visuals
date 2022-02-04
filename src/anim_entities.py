import math
import matplotlib as mpl
from matplotlib.transforms import Bbox
import matplotlib.pyplot as plt


FRAMES_PER_PART = 12
PARTS = 35

FONT_FAMILY = None

TPUBSUB_LINESTYLE = "--"
PUSHPULL_LINESTYLE = ":"
APUBSUB_LINESTYLE = ":"

TPUBSUB_SOCK_COLOR = "#ff0000"
TPUBSUB_LINE_COLOR = "#c00000"
PUSHPULL_SOCK_COLOR = "#ff00ff"
PUSHPULL_LINE_COLOR = "#c000c0"
APUBSUB_SOCK_COLOR = "#ffff00"
APUBSUB_LINE_COLOR = "#c0c000"

BEACON_INTERVAL = 2/3
ADDRESS_INTERVAL = 1/2
ETALE_INTERVAL = 3/4

BEACON_SPEED = 1/2
ADDRESS_SPEED = 1/2
ETALE_SPEED = 1/3

SOCK_RAD = 1/5

BEACON_RAD = 1/2
ADDRESS_RAD = 1/2
ETALE_RAD = 2/3

BEACON_COLOR = "#e000e0"
ADDRESS_COLOR = "#e0e000"
ETALE_COLOR = "#e00000"
ETALE_KEPT_COLOR = "#b00000"

BEACON_SYMBOL = "B"
ADDRESS_SYMBOL = "A"
ETALE_SYMBOL = "T"


PART_EF2_EF3_CONNECTED = 1
PART_EF2_EF3_ETALES_EMITTED = PART_EF2_EF3_CONNECTED + 1

PART_CONNECTED_WITH_ECATAL1 = PART_EF2_EF3_ETALES_EMITTED + 4
PART_CONNECTED_WITH_ECATAL2 = PART_CONNECTED_WITH_ECATAL1 + 8
PART_BEACONS_ECATAL1_STARTED = PART_CONNECTED_WITH_ECATAL1 + 1
PART_BEACONS_ECATAL2_STARTED = PART_CONNECTED_WITH_ECATAL2 + 1
PART_ADDRESSES_ECATAL1_EMITTED = PART_BEACONS_ECATAL1_STARTED + 2
PART_ADDRESSES_ECATAL2_EMITTED = PART_BEACONS_ECATAL2_STARTED + 2
PART_EFUNGI_CONNECTED = min(PART_ADDRESSES_ECATAL1_EMITTED, PART_ADDRESSES_ECATAL2_EMITTED) + 2 + 1
PART_ETALES_EMITTED = PART_EFUNGI_CONNECTED + 1

PART_EF1_RELOC = PART_ADDRESSES_ECATAL2_EMITTED + 4
PART_EF1_RECONN_EC1 = PART_EF1_RELOC + 4
PART_EF1_RECONN_EC2 = PART_EF1_RELOC + 2
PART_EF1_RECONN_BEACONS_EC1 = PART_EF1_RECONN_EC1 + 1
PART_EF1_RECONN_BEACONS_EC2 = PART_EF1_RECONN_EC2 + 1
PART_EF1_RECONN_ADDRESSES_EC1 = PART_EF1_RECONN_EC1 + 1
PART_EF1_RECONN_ADDRESSES_EC2 = PART_EF1_RECONN_EC2 + 1
PART_EF1_RECONN_PUB = min(PART_EF1_RECONN_BEACONS_EC1, PART_EF1_RECONN_BEACONS_EC2) + 2 + 2 + 1
PART_EF1_RECONN_ETALES_EMITTED = PART_EF1_RECONN_PUB + 1

PART_EC1_DISAPPEAR = PART_EF1_RECONN_ETALES_EMITTED + 4


def draw_databall(ax, x, y, radius, color, caption):
	ax.add_patch(plt.Circle((x, y), radius, color=color))
	ax.text(x, y, caption, ha="center", va="center", color="#000000", family=FONT_FAMILY)


def draw_databalls_flow(ax, x0, y0, x1, y1, t_start, interval, speed, t, radius, color, caption):
	k = max(0, math.ceil((t - t_start - 1/speed) / interval))
	t_ball_start = t_start + k * interval
	pos_ball = (t - t_ball_start) * speed

	while pos_ball >= 0.0:
		bx = (1.0 - pos_ball) * x0 + pos_ball * x1
		by = (1.0 - pos_ball) * y0 + pos_ball * y1
		draw_databall(ax, bx, by, radius, color, caption)

		t_ball_start += interval
		pos_ball = (t - t_ball_start) * speed


def make_save_frame(f):
	t = f / FRAMES_PER_PART

	part = f // FRAMES_PER_PART
	# 0   start, no connections
	# 1   efungi <-> ecatals pushpull and address-pubsub conns

	fig, ax = plt.subplots()

	fig.patch.set_facecolor("#000000")

	ax.axis(False)

	ax.set_aspect(1.0)

	fig_min_x = -15.6
	fig_max_x = 13.4

	ax.set_xlim(fig_min_x, fig_max_x)
	ax.set_ylim(-11.2, 11.3)

	# Realms

	# Realm 1 (top)
	ax.add_patch(plt.Rectangle((-5, 6), 10, 8, facecolor="#100808", edgecolor="#201010", linewidth=3))
	ax.text(0, 5.25, "Realm 1", ha="center", va="center", color="#707070", family=FONT_FAMILY)

	# Realm 2 (bottom left)
	ax.add_patch(plt.Rectangle((-16, -12), 8.5, 6.5, facecolor="#081008", edgecolor="#102010", linewidth=3))
	ax.text(-13.5, -5, "Realm 2", ha="center", va="center", color="#707070", family=FONT_FAMILY)

	# Realm 3 (bottom right)
	ax.add_patch(plt.Rectangle((7.5, -12), 8, 6.5, facecolor="#080810", edgecolor="#101020", linewidth=3))
	ax.text(11.5, -5, "Realm 3", ha="center", va="center", color="#707070", family=FONT_FAMILY)

	# Efungi

	# Efunguz 1 (top)
	if part < PART_EF1_RELOC:
		ef1_x = -2
		ef1_y = 8
	else:
		ef1_x = 2
		ef1_y = 8
	ef1_tpub_x = ef1_x - 1
	ef1_tpub_y = ef1_y + 1
	ef1_tsub_x = ef1_x + 1
	ef1_tsub_y = ef1_y + 1
	ef1_push_x = ef1_x - 1/2
	ef1_push_y = ef1_y - 1
	ef1_asub_x = ef1_x + 1/2
	ef1_asub_y = ef1_y - 1
	ax.add_patch(plt.Rectangle((ef1_x-1, ef1_y-1), 2, 2, facecolor="#004000", edgecolor="#00c000", linewidth=2))
	ax.text(ef1_x, ef1_y+2, "Efunguz 1", ha="center", va="center", color="#e0e0e0", family=FONT_FAMILY)
	ax.add_patch(plt.Circle((ef1_tpub_x, ef1_tpub_y), SOCK_RAD, color=TPUBSUB_SOCK_COLOR))
	ax.add_patch(plt.Circle((ef1_tsub_x, ef1_tsub_y), SOCK_RAD, color=TPUBSUB_SOCK_COLOR))
	ax.add_patch(plt.Circle((ef1_push_x, ef1_push_y), SOCK_RAD, color=PUSHPULL_SOCK_COLOR))
	ax.add_patch(plt.Circle((ef1_asub_x, ef1_asub_y), SOCK_RAD, color=APUBSUB_SOCK_COLOR))

	# Efunguz 2 (bottom left)
	ef2_x = -10
	ef2_y = -8
	ef2_tpub_x = ef2_x + 1
	ef2_tpub_y = ef2_y - 1
	ef2_tsub_x = ef2_x - 1
	ef2_tsub_y = ef2_y + 1
	ef2_push_x = ef2_x + 1/2
	ef2_push_y = ef2_y + 1
	ef2_asub_x = ef2_x + 1
	ef2_asub_y = ef2_y + 1/2
	ax.add_patch(plt.Rectangle((ef2_x-1, ef2_y-1), 2, 2, facecolor="#004000", edgecolor="#00c000", linewidth=2))
	ax.text(ef2_x, ef2_y-2, "Efunguz 2", ha="center", va="center", color="#e0e0e0", family=FONT_FAMILY)
	ax.add_patch(plt.Circle((ef2_tpub_x, ef2_tpub_y), SOCK_RAD, color=TPUBSUB_SOCK_COLOR))
	ax.add_patch(plt.Circle((ef2_tsub_x, ef2_tsub_y), SOCK_RAD, color=TPUBSUB_SOCK_COLOR))
	ax.add_patch(plt.Circle((ef2_push_x, ef2_push_y), SOCK_RAD, color=PUSHPULL_SOCK_COLOR))
	ax.add_patch(plt.Circle((ef2_asub_x, ef2_asub_y), SOCK_RAD, color=APUBSUB_SOCK_COLOR))

	# Efunguz 3 (bottom right)
	ef3_x = 10
	ef3_y = -8
	ef3_tpub_x = ef3_x + 1
	ef3_tpub_y = ef3_y + 1
	ef3_tsub_x = ef3_x - 1
	ef3_tsub_y = ef3_y - 1
	ef3_push_x = ef3_x - 1
	ef3_push_y = ef3_y + 1/2
	ef3_asub_x = ef3_x - 1/2
	ef3_asub_y = ef3_y + 1
	ax.add_patch(plt.Rectangle((ef3_x-1, ef3_y-1), 2, 2, facecolor="#004000", edgecolor="#00c000", linewidth=2))
	ax.text(ef3_x, ef3_y-2, "Efunguz 3", ha="center", va="center", color="#e0e0e0", family=FONT_FAMILY)
	ax.add_patch(plt.Circle((ef3_tpub_x, ef3_tpub_y), SOCK_RAD, color=TPUBSUB_SOCK_COLOR))
	ax.add_patch(plt.Circle((ef3_tsub_x, ef3_tsub_y), SOCK_RAD, color=TPUBSUB_SOCK_COLOR))
	ax.add_patch(plt.Circle((ef3_push_x, ef3_push_y), SOCK_RAD, color=PUSHPULL_SOCK_COLOR))
	ax.add_patch(plt.Circle((ef3_asub_x, ef3_asub_y), SOCK_RAD, color=APUBSUB_SOCK_COLOR))

	# Ecataloguzes

	# Ecataloguz 1 (left)
	if part < PART_EC1_DISAPPEAR:
		ec1_x = -3
		ec1_y = -3
		ec1_pull_x = ec1_x - 1/2
		ec1_pull_y = ec1_y
		ec1_apub_x = ec1_x + 1/2
		ec1_apub_y = ec1_y
		ax.add_patch(plt.Rectangle((ec1_x-1, ec1_y-1), 2, 2, facecolor="#000040", edgecolor="#0000c0", linewidth=2))
		ax.text(ec1_x, ec1_y-2, "Ecataloguz 1", ha="center", va="center", color="#e0e0e0", family=FONT_FAMILY)
		ax.add_patch(plt.Circle((ec1_pull_x, ec1_pull_y), SOCK_RAD, color=PUSHPULL_SOCK_COLOR))
		ax.add_patch(plt.Circle((ec1_apub_x, ec1_apub_y), SOCK_RAD, color=APUBSUB_SOCK_COLOR))

	# Ecataloguz 2 (right)
	ec2_x = 3
	ec2_y = -3
	ec2_pull_x = ec2_x - 1/2
	ec2_pull_y = ec2_y
	ec2_apub_x = ec2_x + 1/2
	ec2_apub_y = ec2_y
	ax.add_patch(plt.Rectangle((ec2_x-1, ec2_y-1), 2, 2, facecolor="#000040", edgecolor="#0000c0", linewidth=2))
	ax.text(ec2_x, ec2_y+2, "Ecataloguz 2", ha="center", va="center", color="#e0e0e0", family=FONT_FAMILY)
	ax.add_patch(plt.Circle((ec2_pull_x, ec2_pull_y), SOCK_RAD, color=PUSHPULL_SOCK_COLOR))
	ax.add_patch(plt.Circle((ec2_apub_x, ec2_apub_y), SOCK_RAD, color=APUBSUB_SOCK_COLOR))

	# Ehyphae (etale pubsub connections)

	if ((part < PART_EF1_RELOC) and (part >= PART_EFUNGI_CONNECTED)) or ((part >= PART_EF1_RELOC) and (part >= PART_EF1_RECONN_PUB)):
		# 2 <- 1, 3 <- 1
		ax.plot((ef1_tpub_x, ef2_tsub_x), (ef1_tpub_y, ef2_tsub_y), color=TPUBSUB_LINE_COLOR, linewidth=1, linestyle=TPUBSUB_LINESTYLE)
		ax.plot((ef1_tpub_x, ef3_tsub_x), (ef1_tpub_y, ef3_tsub_y), color=TPUBSUB_LINE_COLOR, linewidth=1, linestyle=TPUBSUB_LINESTYLE)

	if part >= PART_EFUNGI_CONNECTED:
		# 1 <- 2
		ax.plot((ef2_tpub_x, ef1_tsub_x), (ef2_tpub_y, ef1_tsub_y), color=TPUBSUB_LINE_COLOR, linewidth=1, linestyle=TPUBSUB_LINESTYLE)

		# 1 <- 3
		ax.plot((ef3_tpub_x, ef1_tsub_x), (ef3_tpub_y, ef1_tsub_y), color=TPUBSUB_LINE_COLOR, linewidth=1, linestyle=TPUBSUB_LINESTYLE)

	if (part >= PART_EF2_EF3_CONNECTED):
		# 2 <-> 3
		ax.plot((ef2_tpub_x, ef3_tsub_x), (ef2_tpub_y, ef3_tsub_y), color=TPUBSUB_LINE_COLOR, linewidth=1, linestyle=TPUBSUB_LINESTYLE)
		ax.plot((ef3_tpub_x, ef2_tsub_x), (ef3_tpub_y, ef2_tsub_y), color=TPUBSUB_LINE_COLOR, linewidth=1, linestyle=TPUBSUB_LINESTYLE)

	# Etales on ehyphae conns

	# 1 <-> 2, 1 <-> 3
	if ((part < PART_EF1_RELOC) and (part >= PART_ETALES_EMITTED)) or ((part >= PART_EF1_RELOC) and (part >= PART_EF1_RECONN_ETALES_EMITTED)):
		if part < PART_EF1_RELOC:
			t_flow_start = PART_ETALES_EMITTED
		else:
			t_flow_start = PART_EF1_RECONN_ETALES_EMITTED
		# 2 <- 1
		draw_databalls_flow(ax, ef1_tpub_x, ef1_tpub_y, ef2_tsub_x, ef2_tsub_y, t_flow_start, ETALE_INTERVAL, ETALE_SPEED, t, ETALE_RAD, ETALE_COLOR, ETALE_SYMBOL)
		# 3 <- 1
		draw_databalls_flow(ax, ef1_tpub_x, ef1_tpub_y, ef3_tsub_x, ef3_tsub_y, t_flow_start, ETALE_INTERVAL, ETALE_SPEED, t, ETALE_RAD, ETALE_COLOR, ETALE_SYMBOL)

	if part >= PART_ETALES_EMITTED:
		# 1 <- 2
		draw_databalls_flow(ax, ef2_tpub_x, ef2_tpub_y, ef1_tsub_x, ef1_tsub_y, PART_ETALES_EMITTED, ETALE_INTERVAL, ETALE_SPEED, t, ETALE_RAD, ETALE_COLOR, ETALE_SYMBOL)

		# 1 <- 3
		draw_databalls_flow(ax, ef3_tpub_x, ef3_tpub_y, ef1_tsub_x, ef1_tsub_y, PART_ETALES_EMITTED, ETALE_INTERVAL, ETALE_SPEED, t, ETALE_RAD, ETALE_COLOR, ETALE_SYMBOL)

	if part >= PART_EF2_EF3_ETALES_EMITTED:
		# 2 <-> 3
		draw_databalls_flow(ax, ef2_tpub_x, ef2_tpub_y, ef3_tsub_x, ef3_tsub_y, PART_EF2_EF3_ETALES_EMITTED, ETALE_INTERVAL, ETALE_SPEED, t, ETALE_RAD, ETALE_COLOR, ETALE_SYMBOL)
		draw_databalls_flow(ax, ef3_tpub_x, ef3_tpub_y, ef2_tsub_x, ef2_tsub_y, PART_EF2_EF3_ETALES_EMITTED, ETALE_INTERVAL, ETALE_SPEED, t, ETALE_RAD, ETALE_COLOR, ETALE_SYMBOL)

	# Absorbed etales kept at efungi

	if part >= PART_ETALES_EMITTED + int(round(1.0 / ETALE_SPEED)):
		draw_databall(ax, ef1_tsub_x, ef1_tsub_y, ETALE_RAD * 1.4, ETALE_KEPT_COLOR, ETALE_SYMBOL)

	if part >= PART_EF2_EF3_ETALES_EMITTED + int(round(1.0 / ETALE_SPEED)):
		draw_databall(ax, ef2_tsub_x, ef2_tsub_y, ETALE_RAD * 1.4, ETALE_KEPT_COLOR, ETALE_SYMBOL)
		draw_databall(ax, ef3_tsub_x, ef3_tsub_y, ETALE_RAD * 1.4, ETALE_KEPT_COLOR, ETALE_SYMBOL)

	# Pushpull conns

	if ((part < PART_EF1_RELOC) and (part >= PART_CONNECTED_WITH_ECATAL1)) or ((part >= PART_EF1_RELOC) and (part >= PART_EF1_RECONN_EC1) and (part < PART_EC1_DISAPPEAR)):
		ax.plot((ef1_push_x, ec1_pull_x), (ef1_push_y, ec1_pull_y), color=PUSHPULL_LINE_COLOR, linewidth=1, linestyle=PUSHPULL_LINESTYLE)

	if (part >= PART_CONNECTED_WITH_ECATAL1) and (part < PART_EC1_DISAPPEAR):
		ax.plot((ef2_push_x, ec1_pull_x), (ef2_push_y, ec1_pull_y), color=PUSHPULL_LINE_COLOR, linewidth=1, linestyle=PUSHPULL_LINESTYLE)
		ax.plot((ef3_push_x, ec1_pull_x), (ef3_push_y, ec1_pull_y), color=PUSHPULL_LINE_COLOR, linewidth=1, linestyle=PUSHPULL_LINESTYLE)

	if ((part < PART_EF1_RELOC) and (part >= PART_CONNECTED_WITH_ECATAL2)) or ((part >= PART_EF1_RELOC) and (part >= PART_EF1_RECONN_EC2)):
		ax.plot((ef1_push_x, ec2_pull_x), (ef1_push_y, ec2_pull_y), color=PUSHPULL_LINE_COLOR, linewidth=1, linestyle=PUSHPULL_LINESTYLE)

	if part >= PART_CONNECTED_WITH_ECATAL2:
		ax.plot((ef2_push_x, ec2_pull_x), (ef2_push_y, ec2_pull_y), color=PUSHPULL_LINE_COLOR, linewidth=1, linestyle=PUSHPULL_LINESTYLE)
		ax.plot((ef3_push_x, ec2_pull_x), (ef3_push_y, ec2_pull_y), color=PUSHPULL_LINE_COLOR, linewidth=1, linestyle=PUSHPULL_LINESTYLE)

	# Beacons on pushpull conns

	if ((part < PART_EF1_RELOC) and (part >= PART_BEACONS_ECATAL1_STARTED)) or ((part >= PART_EF1_RELOC) and (part >= PART_EF1_RECONN_BEACONS_EC1) and (part < PART_EC1_DISAPPEAR)):
		if part < PART_EF1_RELOC:
			t_flow_start = PART_BEACONS_ECATAL1_STARTED
		else:
			t_flow_start = PART_EF1_RECONN_BEACONS_EC1
		draw_databalls_flow(ax, ef1_push_x, ef1_push_y, ec1_pull_x, ec1_pull_y, t_flow_start, BEACON_INTERVAL, BEACON_SPEED, t, BEACON_RAD, BEACON_COLOR, BEACON_SYMBOL)

	if (part >= PART_BEACONS_ECATAL1_STARTED) and (part < PART_EC1_DISAPPEAR):
		draw_databalls_flow(ax, ef2_push_x, ef2_push_y, ec1_pull_x, ec1_pull_y, PART_BEACONS_ECATAL1_STARTED, BEACON_INTERVAL, BEACON_SPEED, t, BEACON_RAD, BEACON_COLOR, BEACON_SYMBOL)
		draw_databalls_flow(ax, ef3_push_x, ef3_push_y, ec1_pull_x, ec1_pull_y, PART_BEACONS_ECATAL1_STARTED, BEACON_INTERVAL, BEACON_SPEED, t, BEACON_RAD, BEACON_COLOR, BEACON_SYMBOL)

	if ((part < PART_EF1_RELOC) and (part >= PART_BEACONS_ECATAL2_STARTED)) or ((part >= PART_EF1_RELOC) and (part >= PART_EF1_RECONN_BEACONS_EC2)):
		if part < PART_EF1_RELOC:
			t_flow_start = PART_BEACONS_ECATAL2_STARTED
		else:
			t_flow_start = PART_EF1_RECONN_BEACONS_EC2
		draw_databalls_flow(ax, ef1_push_x, ef1_push_y, ec2_pull_x, ec2_pull_y, t_flow_start, BEACON_INTERVAL, BEACON_SPEED, t, BEACON_RAD, BEACON_COLOR, BEACON_SYMBOL)

	if part >= PART_BEACONS_ECATAL2_STARTED:
		draw_databalls_flow(ax, ef2_push_x, ef2_push_y, ec2_pull_x, ec2_pull_y, PART_BEACONS_ECATAL2_STARTED, BEACON_INTERVAL, BEACON_SPEED, t, BEACON_RAD, BEACON_COLOR, BEACON_SYMBOL)
		draw_databalls_flow(ax, ef3_push_x, ef3_push_y, ec2_pull_x, ec2_pull_y, PART_BEACONS_ECATAL2_STARTED, BEACON_INTERVAL, BEACON_SPEED, t, BEACON_RAD, BEACON_COLOR, BEACON_SYMBOL)

	# Address-pubsub conns

	if ((part < PART_EF1_RELOC) and (part >= PART_CONNECTED_WITH_ECATAL1)) or ((part >= PART_EF1_RELOC) and (part >= PART_EF1_RECONN_EC1) and (part < PART_EC1_DISAPPEAR)):
		ax.plot((ec1_apub_x, ef1_asub_x), (ec1_apub_y, ef1_asub_y), color=APUBSUB_LINE_COLOR, linewidth=1, linestyle=APUBSUB_LINESTYLE)

	if (part >= PART_CONNECTED_WITH_ECATAL1) and (part < PART_EC1_DISAPPEAR):
		ax.plot((ec1_apub_x, ef2_asub_x), (ec1_apub_y, ef2_asub_y), color=APUBSUB_LINE_COLOR, linewidth=1, linestyle=APUBSUB_LINESTYLE)
		ax.plot((ec1_apub_x, ef3_asub_x), (ec1_apub_y, ef3_asub_y), color=APUBSUB_LINE_COLOR, linewidth=1, linestyle=APUBSUB_LINESTYLE)

	if ((part < PART_EF1_RELOC) and (part >= PART_CONNECTED_WITH_ECATAL2)) or ((part >= PART_EF1_RELOC) and (part >= PART_EF1_RECONN_EC2)):
		ax.plot((ec2_apub_x, ef1_asub_x), (ec2_apub_y, ef1_asub_y), color=APUBSUB_LINE_COLOR, linewidth=1, linestyle=APUBSUB_LINESTYLE)

	if part >= PART_CONNECTED_WITH_ECATAL2:
		ax.plot((ec2_apub_x, ef2_asub_x), (ec2_apub_y, ef2_asub_y), color=APUBSUB_LINE_COLOR, linewidth=1, linestyle=APUBSUB_LINESTYLE)
		ax.plot((ec2_apub_x, ef3_asub_x), (ec2_apub_y, ef3_asub_y), color=APUBSUB_LINE_COLOR, linewidth=1, linestyle=APUBSUB_LINESTYLE)

	# Addresses data on address-pubsub conns

	if ((part < PART_EF1_RELOC) and (part >= PART_ADDRESSES_ECATAL1_EMITTED)) or ((part >= PART_EF1_RELOC) and (part >= PART_EF1_RECONN_ADDRESSES_EC1) and (part < PART_EC1_DISAPPEAR)):
		if part < PART_EF1_RELOC:
			t_flow_start = PART_ADDRESSES_ECATAL1_EMITTED
		else:
			t_flow_start = PART_EF1_RECONN_ADDRESSES_EC1
		draw_databalls_flow(ax, ec1_apub_x, ec1_apub_y, ef1_asub_x, ef1_asub_y, t_flow_start, ADDRESS_INTERVAL, ADDRESS_SPEED, t, ADDRESS_RAD, ADDRESS_COLOR, ADDRESS_SYMBOL)

	if (part >= PART_ADDRESSES_ECATAL1_EMITTED) and (part < PART_EC1_DISAPPEAR):
		draw_databalls_flow(ax, ec1_apub_x, ec1_apub_y, ef2_asub_x, ef2_asub_y, PART_ADDRESSES_ECATAL1_EMITTED, ADDRESS_INTERVAL, ADDRESS_SPEED, t, ADDRESS_RAD, ADDRESS_COLOR, ADDRESS_SYMBOL)
		draw_databalls_flow(ax, ec1_apub_x, ec1_apub_y, ef3_asub_x, ef3_asub_y, PART_ADDRESSES_ECATAL1_EMITTED, ADDRESS_INTERVAL, ADDRESS_SPEED, t, ADDRESS_RAD, ADDRESS_COLOR, ADDRESS_SYMBOL)

	if ((part < PART_EF1_RELOC) and (part >= PART_ADDRESSES_ECATAL2_EMITTED)) or ((part >= PART_EF1_RELOC) and (part >= PART_EF1_RECONN_ADDRESSES_EC2)):
		if part < PART_EF1_RELOC:
			t_flow_start = PART_ADDRESSES_ECATAL2_EMITTED
		else:
			t_flow_start = PART_EF1_RECONN_ADDRESSES_EC2
		draw_databalls_flow(ax, ec2_apub_x, ec2_apub_y, ef1_asub_x, ef1_asub_y, t_flow_start, ADDRESS_INTERVAL, ADDRESS_SPEED, t, ADDRESS_RAD, ADDRESS_COLOR, ADDRESS_SYMBOL)

	if part >= PART_ADDRESSES_ECATAL2_EMITTED:
		draw_databalls_flow(ax, ec2_apub_x, ec2_apub_y, ef2_asub_x, ef2_asub_y, PART_ADDRESSES_ECATAL2_EMITTED, ADDRESS_INTERVAL, ADDRESS_SPEED, t, ADDRESS_RAD, ADDRESS_COLOR, ADDRESS_SYMBOL)
		draw_databalls_flow(ax, ec2_apub_x, ec2_apub_y, ef3_asub_x, ef3_asub_y, PART_ADDRESSES_ECATAL2_EMITTED, ADDRESS_INTERVAL, ADDRESS_SPEED, t, ADDRESS_RAD, ADDRESS_COLOR, ADDRESS_SYMBOL)

	# Legend of lines

	lgndL_x = -14.0
	lgndL_y = 9.5

	ax.add_patch(plt.Rectangle((lgndL_x - 0.75, lgndL_y - 8.75), 5.5, 9.5, facecolor="#000000", edgecolor="#404040", linestyle="--"))

	ax.add_patch(plt.Circle((lgndL_x, lgndL_y), SOCK_RAD, color=PUSHPULL_SOCK_COLOR))
	ax.add_patch(plt.Circle((lgndL_x + 4, lgndL_y), SOCK_RAD, color=PUSHPULL_SOCK_COLOR))
	ax.plot((lgndL_x, lgndL_x + 4), (lgndL_y, lgndL_y), color=PUSHPULL_LINE_COLOR, linewidth=1, linestyle=PUSHPULL_LINESTYLE)
	ax.text(lgndL_x, lgndL_y - 1, "PUSH-PULL", va="center", color="#c0c0c0", family=FONT_FAMILY)

	ax.add_patch(plt.Circle((lgndL_x, lgndL_y - 3), SOCK_RAD, color=APUBSUB_SOCK_COLOR))
	ax.add_patch(plt.Circle((lgndL_x + 4, lgndL_y - 3), SOCK_RAD, color=APUBSUB_SOCK_COLOR))
	ax.plot((lgndL_x, lgndL_x + 4), (lgndL_y - 3, lgndL_y - 3), color=APUBSUB_LINE_COLOR, linewidth=1, linestyle=APUBSUB_LINESTYLE)
	ax.text(lgndL_x, lgndL_y - 4, "PUB-SUB", va="center", color="#c0c0c0", family=FONT_FAMILY)

	ax.add_patch(plt.Circle((lgndL_x, lgndL_y - 6), SOCK_RAD, color=TPUBSUB_SOCK_COLOR))
	ax.add_patch(plt.Circle((lgndL_x + 4, lgndL_y - 6), SOCK_RAD, color=TPUBSUB_SOCK_COLOR))
	ax.plot((lgndL_x, lgndL_x + 4), (lgndL_y - 6, lgndL_y - 6), color=TPUBSUB_LINE_COLOR, linewidth=1, linestyle=TPUBSUB_LINESTYLE)
	ax.text(lgndL_x, lgndL_y - 7, "Ehypha", va="center", color="#c0c0c0", family=FONT_FAMILY)
	ax.text(lgndL_x, lgndL_y - 8, "PUB-SUB", va="center", color="#c0c0c0", family=FONT_FAMILY)

	# Legend of balls

	lgndB_x = 8.0
	lgndB_y = 9.0

	ax.add_patch(plt.Rectangle((lgndB_x - 1.25, lgndB_y - 5.25), 5.75, 6.5, facecolor="#000000", edgecolor="#404040", linestyle="--"))

	draw_databall(ax, lgndB_x, lgndB_y, BEACON_RAD, BEACON_COLOR, BEACON_SYMBOL)
	ax.text(lgndB_x + 1, lgndB_y, "beacon", ha="left", va="center", color="#c0c0c0", family=FONT_FAMILY)

	draw_databall(ax, lgndB_x, lgndB_y - 2, ADDRESS_RAD, ADDRESS_COLOR, ADDRESS_SYMBOL)
	ax.text(lgndB_x + 1, lgndB_y - 2, "address", ha="left", va="center", color="#c0c0c0", family=FONT_FAMILY)

	draw_databall(ax, lgndB_x, lgndB_y - 4, ETALE_RAD, ETALE_COLOR, ETALE_SYMBOL)
	ax.text(lgndB_x + 1, lgndB_y - 4, "Etale", ha="left", va="center", color="#c0c0c0", family=FONT_FAMILY)

	# Timeline

	ax.add_patch(plt.Rectangle((fig_min_x, 11.1), (fig_max_x - fig_min_x) * (f + 1) / (PARTS * FRAMES_PER_PART), 1, color="#008080"))

	# fig.savefig(f"frames/frame_{f:03}.png", dpi=100, bbox_inches="tight", pad_inches=0)
	# print(fig.get_tightbbox(fig.canvas.get_renderer()))
	fig.savefig(f"frames/frame_{(f+1):03}.png", dpi=100, bbox_inches=Bbox([[0.9, 0.59], [5.66, 4.23]]))

	plt.close(fig)


def main():
	start = 0
	end = PARTS * FRAMES_PER_PART
	for f in range(start, end):
		print(f"\rMaking frame {(f+1):4} / {(end - start):4} ... ", end="")
		make_save_frame(f)
		print("OK.", end="")
	print("")


main()
