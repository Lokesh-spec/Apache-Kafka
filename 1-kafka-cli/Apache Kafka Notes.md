
## **Introduction**

- Apache Kafka is an **open-source distributed streaming platform**.
- It allows applications to **produce**, **consume**, and **analyze streaming data in real-time**.

---

## **Key Concepts**

### **1. Kafka Topics**

- Topics are **immutable**, meaning once data is written to a partition, it **cannot be changed**.
- Data in a topic is stored for a **limited time** (default: 1 week, configurable).
- **Offsets**:
    - Each message within a partition has a unique **offset**.
    - Offsets are meaningful only within the **specific partition** they belong to.
    - Offsets are not reused, even after messages are deleted.

### **2. Partitions**

- Topics are split into **partitions** to enhance scalability.
- Characteristics:
    1. Messages within a partition are **ordered**.
    2. Data is assigned to partitions **randomly**, unless a **key** is specified.
    3. A partition guarantees **ordering** of messages but not across partitions.

---

### **3. Kafka Producers**

- Producers are responsible for **writing data** to topics.
- Producers understand which **partition** and **broker** to write to.
- **Key Characteristics**:
    1. Producers can optionally send a **key** with messages.
        - If `key=null`: Data is sent to partitions in a **round-robin** manner.
        - If `key!=null`: Messages with the same key always go to the **same partition**.
    2. Producers handle failures automatically and retry if a broker is unavailable.

### **4. Kafka Consumers**

- Consumers **read data** from topics in a **pull model**.
- Characteristics:
    1. Consumers fetch data from partitions in **offset order**.
    2. They handle broker failures automatically to ensure reliable data fetching.

---

## **Serialization and Deserialization**

### **1. Serialization (Producers)**

- Kafka only accepts **byte arrays** as input and output.
- Serialization is the process of converting **objects or data** into bytes.
- Common Serializers:
    1. **String** (e.g., JSON)
    2. **Integer/Float**
    3. **Avro**
    4. **Protobuf**

### **2. Deserialization (Consumers)**

- Consumers use deserialization to convert **bytes back into objects** or data.
- Common Deserializers:
    1. **String**
    2. **Integer/Float**
    3. **Avro**
    4. **Protobuf**

---

## **Kafka Brokers**

- Kafka clusters are composed of multiple **brokers**.
- Characteristics:
    1. Each broker is identified by a **unique ID**.
    2. Brokers host topic **partitions**.
    3. Connecting to any broker (bootstrap broker) connects the client to the **entire cluster**.

---

## **Kafka CLI Commands**

### **1. Create Topics**

``` bash
# Create a topic
kafka-topics.sh --bootstrap-server localhost:9092 --topic first_topic --create

# Create a topic with partitions
kafka-topics.sh --bootstrap-server localhost:9092 --topic second_topic --create --partitions 3

# Create a topic with partitions and replication factor
kafka-topics.sh --bootstrap-server localhost:9092 --topic third_topic --create --partitions 3 --replication-factor 2
```

### **2. List Topics**

``` bash
kafka-topics.sh --bootstrap-server localhost:9092 --list
```

### **3. Describe Topics**

``` bash
kafka-topics.sh --bootstrap-server localhost:9092 --topic first_topic --describe
```

### **4. Delete Topics**

``` bash
# Delete a topic (requires delete.topic.enable=true)
kafka-topics.sh --bootstrap-server localhost:9092 --topic first_topic --delete
```


---

### **Example: Truck GPS Data**

- **Scenario**: A fleet of trucks reports GPS data to Kafka.
    1. Each truck sends a message every 20 seconds with:
        - **Truck ID**
        - **Position (latitude/longitude)**
    2. The data is sent to a topic named `trucks-gps` with **10 partitions**.

**Important Notes**:

1. Data is **immutable** once written to a partition.
2. Messages with the same **truck ID** are sent to the same partition (for ordering).