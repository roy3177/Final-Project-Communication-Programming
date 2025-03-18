import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the CSV
df = pd.read_csv('youtube_filtered.csv')

# 2. Convert Time to numeric if needed
df['Time'] = pd.to_numeric(df['Time'], errors='coerce')
df = df.sort_values('Time').reset_index(drop=True)

##############################################################################
# 1) IP Address Distribution (Source vs. Destination) - Improved Readability
##############################################################################
source_counts = df['Source'].value_counts()
dest_counts = df['Destination'].value_counts()

plt.figure(figsize=(10, 5))
width = 0.4  # Width for bars
x = range(len(source_counts.index[:10]))
plt.bar(x, source_counts.values[:10], width=width, label='Source IPs', color='steelblue')
plt.bar([i + width for i in x], dest_counts.values[:10], width=width, label='Destination IPs', color='darkorange')
plt.xticks([i + width / 2 for i in x], source_counts.index[:10], rotation=45)
plt.title('Top 10 IPs (Source vs. Destination)')
plt.legend()
plt.tight_layout()
plt.show()

##############################################################################
# 2) TCP Flags Analysis
##############################################################################
flag_counts = df['Flags'].value_counts()

plt.figure(figsize=(8, 5))
plt.bar(flag_counts.index, flag_counts.values, color='green')
plt.title('TCP Flags Distribution')
plt.xlabel('Flags')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

##############################################################################
# 3) TLS Header Fields Analysis
##############################################################################
if 'TLS Server Name' in df.columns and df['TLS Server Name'].notna().any():
    tls_counts = df['TLS Server Name'].value_counts()
    plt.figure(figsize=(8, 5))
    plt.bar(tls_counts.index[:10], tls_counts.values[:10], color='purple')
    plt.title('Top 10 TLS Server Names')
    plt.xlabel('TLS Server Name')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("No TLS Server Name data available or column missing.")

##############################################################################
# 4) Packet Size Distribution - Improved Readability
##############################################################################
plt.figure(figsize=(10, 6))
plt.hist(df['Length'], bins=30, color='teal', edgecolor='black', alpha=0.75)
plt.yscale('log')  # Log scale for better visibility of smaller counts
plt.title('Packet Size Distribution')
plt.xlabel('Packet Length (bytes)')
plt.ylabel('Count (log scale)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

##############################################################################
# 5) Inter-Packet Time Differences (Line Plot)
##############################################################################
df['time_delta'] = df['Time'].diff().fillna(0)

plt.figure(figsize=(10, 5))
plt.plot(df['Time'], df['time_delta'], color='maroon', alpha=0.7)
plt.title('Inter-Packet Time Over Time')
plt.xlabel('Time (seconds)')
plt.ylabel('Time Delta (seconds)')
plt.tight_layout()
plt.show()

##############################################################################
# 6) Flow Size (Number of Packets per Flow) - Improved Readability
##############################################################################
flow_cols = ['Source', 'Destination', 'Protocol']
if set(flow_cols).issubset(df.columns):
    flow_group = df.groupby(flow_cols)
    flow_size = flow_group.size().reset_index(name='packet_count')
    flow_size_sorted = flow_size.sort_values('packet_count', ascending=False).head(10)

    flows = [f"{row['Source']}→{row['Destination']}({row['Protocol']})" for _, row in flow_size_sorted.iterrows()]

    plt.figure(figsize=(10, 6))
    plt.barh(flows, flow_size_sorted['packet_count'], color='darkcyan')
    plt.title('Top 10 Flows by Packet Count')
    plt.xlabel('Packet Count')
    plt.ylabel('Flow (Src→Dst)')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
else:
    print("Flow columns (Source, Destination, Protocol) not available.")

##############################################################################
# 7) Flow Volume (Total Bytes per Flow)
##############################################################################
if set(flow_cols).issubset(df.columns) and 'Length' in df.columns:
    flow_volume = flow_group['Length'].sum().reset_index(name='total_bytes')
    flow_volume_sorted = flow_volume.sort_values('total_bytes', ascending=False).head(10)
    flows_vol = [f"{row['Source']}→{row['Destination']}({row['Protocol']})" for _, row in flow_volume_sorted.iterrows()]

    plt.figure(figsize=(10, 6))
    plt.barh(flows_vol, flow_volume_sorted['total_bytes'], color='sienna')
    plt.title('Top 10 Flows by Total Bytes')
    plt.xlabel('Total Bytes')
    plt.ylabel('Flow (Src→Dst)')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
else:
    print("Flow volume columns or 'Length' not available.")
