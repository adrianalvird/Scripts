import argparse
import ipaddress

def process_cidr_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            cidr = line.strip()
            network = ipaddress.IPv4Network(cidr, strict=False)
            if network.num_addresses == 1:
                print(network.network_address)
            else:
                for ip in network.hosts():
                    print(ip)

def main():
    parser = argparse.ArgumentParser(description='Extract IP range from IPv4 CIDR notation.')
    parser.add_argument('-cidr', help='IPv4 CIDR notation')
    parser.add_argument('-file', help='File containing IPv4 CIDR notations, one per line')

    args = parser.parse_args()

    if args.cidr:
        network = ipaddress.IPv4Network(args.cidr, strict=False)
        if network.num_addresses == 1:
            print(network.network_address)
        else:
            for ip in network.hosts():
                print(ip)

    elif args.file:
        process_cidr_file(args.file)

    else:
        print("Please provide either -cidr or -file option.")

if __name__ == "__main__":
    main()

