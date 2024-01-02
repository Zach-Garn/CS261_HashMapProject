# Name: Zachary Garner
# OSU Email: garnerz@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: HashMap Implementation
# Due Date: 12/07/2023
# Description: Class for a HashMap data structure that utilizes a DynamicArray for storage. This class uses singly
# linked list chaining for collision resolution.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def items(self):
        """
        Helper function to access all key-value pairs stored in the hash map. Used in the find_mode method.
        """
        for i in range(self._buckets.length()):
            bucket = self._buckets[i]
            for node in bucket:
                yield node.key, node.value

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If the value already exists, then the associated value is replaced
        with the new value. If not, then a new key/value pair is added.

        :param key:   The unique identifier to determine where the new value is stored
        :param value: The object being stored at the key
        """
        # Check the load factor to determine if a resize is necessary
        if self.table_load() >= 1.0:
            self.resize_table(self.get_capacity() * 2)

        # Hash the key and find the bucket
        bucket_index = self._hash_function(key) % self.get_capacity()
        bucket = self._buckets[bucket_index]

        # Check if key exists
        existing_node = bucket.contains(key)

        if existing_node is not None:
            # The key exists so value is updated
            existing_node.value = value
        else:
            # Key does not exist
            bucket.insert(key, value)
            self._size += 1  # Increment if the new value was added

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the table to a new capacity if the current capacity is >= 1.

        :param new_capacity: The new size of the hash table's array
        """
        # Determine if the new_capacity is already < than 1
        if new_capacity < 1:
            return

        # Adjust the capacity to the next prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Create a new hash map for rehashing
        new_hash_map = HashMap(new_capacity, self._hash_function)

        # Fixes an edge case where when capacity = 2 it remains 2 vs changing to 3, since 2 is already prime
        if new_capacity == 2:
            new_hash_map._capacity = 2

        # Rehash the elements to the new hash map
        for i in range(self._capacity):
            bucket = self._buckets[i]
            for node in bucket:
                new_hash_map.put(node.key, node.value)

        # Update the hash map
        self._buckets = new_hash_map._buckets
        self._capacity = new_hash_map._capacity

    def table_load(self) -> float:
        """
        Returns the load factor of the hash table.
        """
        return self.get_size() / self.get_capacity()

    def empty_buckets(self) -> int:
        """
        Returns how many empty buckets are in the hash map.

        :return: The number of empty buckets
        """
        counter = 0

        for i in range(self._buckets.length()):
            bucket = self._buckets[i]
            # Iterate over the list to find empty buckets
            if not any(node for node in bucket):
                counter += 1

        return counter

    def get(self, key: str):
        """
        Returns the value associated with the given key, if the key is not found, it returns None.

        :param key: The given key that is associated with the value to be found
        :return:    The value at the given key or None if the key was not found
        """
        # Find the hash to the correct bucket
        bucket_index = self._hash_function(key) % self.get_capacity()
        bucket = self._buckets[bucket_index]

        # Find the key in the bucket
        node = bucket.contains(key)
        if node is not None:
            return node.value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Checks if the provided key is in the hash map.

        :param key: The target key being searched for
        :return:    True if the key exists, False if it does not
        """
        bucket_index = self._hash_function(key) % self.get_capacity()
        bucket = self._buckets[bucket_index]

        # Traverse and see if the target key exists
        return bucket.contains(key) is not None

    def remove(self, key: str) -> None:
        """
        Removes the key given key and its associated value.

        :param key: The target key to be removed
        """
        # Find the hash to the correct bucket
        bucket_index = self._hash_function(key) % self.get_capacity()
        bucket = self._buckets[bucket_index]

        # Determine if the key exists
        node = bucket.contains(key)

        # Remove the key if it exists
        if node is not None:
            bucket.remove(key)
            # Decrement
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Creates a new DynamicArray where each index is a tuple that contains the key/value pair that's stored in the
        hash map.

        :return: The newly created DynamicArray
        """
        # Initialize a new DynamicArray
        new_da = DynamicArray()

        for i in range(self._buckets.length()):
            bucket = self._buckets[i]
            # Traverse each linked list
            for node in bucket:
                # Create a new tuple for each node
                new_tuple = (node.key, node.value)
                # Append to new_da
                new_da.append(new_tuple)

        return new_da

    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing the underlying capacity of the hash table.

        """
        for i in range(self._buckets.length()):
            # Reset each bucket to an empty LinkedList
            self._buckets[i] = LinkedList()

        # Reset the size
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Standalone function that receives a DynamicArray and returns a tuple containing the mode and an integer that
    represents the highest frequency of occurrences.

    If there is more than one value with the highest frequency, then all values are included in the DynamicArray.

    :param da: The DynamicArray that is received and returns the tuple
    :return:   The DynamicArray containing the tuple
    """
    map = HashMap()

    # Iterate over the DynamicArray
    for i in range(da.length()):
        element = da.get_at_index(i)
        # Retrieve and Increment the frequency
        if map.contains_key(element):
            current_frequency = map.get(element)
            map.put(element, current_frequency + 1)
        else:
            # Add element to the hash map with a frequency of 1
            map.put(element, 1)

    highest_frequency = 0
    mode_values = DynamicArray()

    # Iterate over map to find the highest frequency and mode
    for key, value in map.items():
        if value > highest_frequency:
            highest_frequency = value
            mode_values = DynamicArray()
            mode_values.append(key)
        elif value == highest_frequency:
            mode_values.append(key)

    return mode_values, highest_frequency


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(100)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")

