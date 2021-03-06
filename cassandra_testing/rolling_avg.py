from cassandra.cluster import Cluster
import time
state_list = ["Alabama", "Alaska", "Arizona ", "Arkansas ", "California", "Colorado",
                "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois",
                "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
                "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
                "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
                "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia",
                "Washington", "West Virginia", "Wisconsin", "Wyoming"]


states = [0] * 50
total_seen = [0] * 50

avg_csv = ''
states_csv = ''

cluster = Cluster()
session = cluster.connect('storm')
while(True):
	results = session.execute("SELECT * FROM storm_data")
	for x in results:
	    rows = x
	    state_name = rows[1]
	    state_name = state_name.lower()
	    state_sentiment = rows[2]
	    for i in range(0, len(state_list)):
		state_list[i] = state_list[i].lower()
		if(state_list[i] == state_name):
		    states[i] += float(state_sentiment)
		    total_seen[i] += 1.0



	for i in range(0, len(states)):
	    if(total_seen[i] == 0):
		total_seen[i] = 1
	    average = states[i]/total_seen[i]

            avg_csv = avg_csv + str(average) + ','
            states_csv = states_csv + str(state_list[i]) + ','
            csv_state = open('state_data.csv', 'w')
            csv_avg = open('avg_data.csv', 'w')
            csv_state.write(states_csv)
            csv_avg.write(avg_csv)
            csv_state.close()
            csv_avg.close()

	    insert = session.execute(
		    """
		    INSERT INTO website_data (id, state_name, state_sentiment)
		    VALUES(%s, %s, %s)
		    """,
		    (i, state_list[i], average)
		    )

        time.sleep(30)
