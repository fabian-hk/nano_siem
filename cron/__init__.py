def is_tor_exit_node(input):
    import urllib
    import datetime
    import os
    
    #check if file exits
    if os.path.isfile("/home/vagrant/work/projects/chipwhisperer/tor_exit_nodes.txt"):
        my_file = open("/home/vagrant/work/projects/chipwhisperer/tor_exit_nodes.txt", "r")
        modified_date = datetime.datetime.fromtimestamp(os.path.getmtime('tor_exit_nodes.txt'))
        duration = today - modified_date
        # download new file and replace only if exits more than a day
        if duration.days > 1:
            urllib.request.urlretrieve("https://check.torproject.org/torbulkexitlist", "tor_exit_nodes.txt")
            my_file = open("tor_exit_nodes.txt", "r")
    else:
        my_file = open("/home/vagrant/work/projects/chipwhisperer/tor_exit_nodes.txt", "r")
    data = my_file.read()
    data_into_list = data.split("\n")
    my_file.close()
    if input in data_into_list:
        return True
    else:
        return False
