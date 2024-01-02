# Name: Zachary Garner
# OSU Email: garnerz@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: HashMap Implementation
# Due Date: 12/07/2023
# Description: Class for a HashMap data structure that utilizes a DynamicArray for storage. This class uses open
# addressing with quadratic probing for its collision resolution.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If the key already exists, then the value is updated to the given
        value. If it does not exist then the key/value pair is added. If a resize is necessary, then resize_table is
        called. The function utilizes quadratic probing to find the next empty bucket.

        :param key:   The target key
        :param value: The given value that is to be added
        """
        # Check if a resize is needed
        if self.table_load() >= 0.5:
            self.resize_table(2 * self.get_capacity())

        # Determine the hash index
        index = self._hash_function(key) % self.get_capacity()
        probing = 0

        # Loop to find the correct position for the key
        while True:
            current_index = (index + probing ** 2) % self.get_capacity()
            bucket = self._buckets[current_index]

            # If the bucket is empty or has a tombstone, or contains the same key
            if not bucket or bucket.is_tombstone or bucket.key == key:
                # Add or update the entry
                self._buckets[current_index] = HashEntry(key, value)

                # If it was a new entry, increment size
                if not bucket or bucket.is_tombstone:
                    self._size += 1
                return

            # Increment probing by 1
            probing += 1

            # Prevent infinite loops
            if probing >= self.get_capacity():
                return

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the table if the new_capacity is less than the current number of elements.

        :param new_capacity: The new size of the hash table's array
        """
        # Determine if the new_capacity is less than the current number of elements
        if new_capacity < self.get_size() or new_capacity < 1:
            return

        # Adjust the capacity to the next prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Create a new hash map for rehashing
        new_hash_map = HashMap(new_capacity, self._hash_function)

        # Rehash the elements to the new hash map
        for i in range(self._buckets.length()):
            bucket = self._buckets[i]
            if bucket and not bucket.is_tombstone:
                new_hash_map.put(bucket.key, bucket.value)

        # Update the current hash map to the new hash map
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

        # Iterate through all the buckets
        for i in range(self._buckets.length()):
            # If a bucket is None or a tombstone, counter increments by 1
            if not self._buckets[i] or (self._buckets[i] and self._buckets[i].is_tombstone):
                counter += 1

        return counter

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key, if the key is not found, it returns None.

        :param key: The given key that is associated with the value to be found
        :return:    The value at the given key or None if the key was not found
        """
        # Find the initial hash index for the key
        initial_index = self._hash_function(key) % self.get_capacity()
        index = initial_index
        probing = 0

        while True:
            current = self._buckets[index]

            # If the bucket is empty, the key is not in the hash map
            if current is None:
                return None

            # Check if the bucket has the target key and is not a tombstone
            if current and not current.is_tombstone and current.key == key:
                return current.value

            # Increment probing and recalculate the index
            probing += 1
            index = (initial_index + probing ** 2) % self.get_capacity()

            # End the loop if the key was not found after searching every bucket
            if probing >= self.get_capacity():
                return None

    def contains_key(self, key: str) -> bool:
        """
        Checks if the provided key is in the hash map.

        :param key: The target key being searched for
        :return:    True if the key exists, False if it does not
        """
        # Find the hash to the correct bucket
        initial_index = self._hash_function(key) % self.get_capacity()
        index = initial_index
        probing = 0

        while True:
            bucket = self._buckets[index]

            # If the bucket is empty, the key is not in the hash map
            if bucket is None:
                return False

            # Check if the current bucket has the target key and is not a tombstone
            if bucket and not bucket.is_tombstone and bucket.key == key:
                return True

            # Increment probing and recalculate the index
            probing += 1
            index = (initial_index + probing ** 2) % self.get_capacity()

            # End the loop if the probe count exceeds the hash map's capacity
            if probing >= self.get_capacity():
                return False

    def remove(self, key: str) -> None:
        """
        Removes the key given key and its associated value.

        :param key: The target key to be removed
        """
        # Find the initial hash index for the key
        initial_index = self._hash_function(key) % self.get_capacity()
        index = initial_index
        probing = 0

        while True:
            bucket = self._buckets[index]

            # If the bucket is empty, the key is not in the hash map
            if bucket is None:
                return

            # If the key is found, and it's not a tombstone, mark as removed
            if bucket and not bucket.is_tombstone and bucket.key == key:
                self._buckets[index].is_tombstone = True
                self._size -= 1
                return

            # Increment probing and recalculate the index
            probing += 1
            index = (initial_index + probing ** 2) % self.get_capacity()

            # End the loop if the probe count exceeds the hash map's capacity
            if probing >= self.get_capacity():
                return

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
            # If the bucket is not None and is not a tombstone, add the key/value
            if bucket and not bucket.is_tombstone:
                new_da.append((bucket.key, bucket.value))

        return new_da

    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing the underlying capacity of the hash table.

        """
        # Iterate through all buckets and set them to None
        for i in range(self._buckets.length()):
            self._buckets[i] = None

        # Reset the size to 0
        self._size = 0

    def __iter__(self):
        """
        Allows the hash map to iterate across itself.

        """
        # Initialize index
        self._iter_index = 0
        return self

    def __next__(self):
        """
        Returns the next item in the hash map based on the location of the iterator.

        """
        while self._iter_index < self._buckets.length():
            bucket = self._buckets[self._iter_index]
            self._iter_index += 1

            # Only return values that are not None or a tombstone
            if bucket is not None and not bucket.is_tombstone:
                return bucket

        raise StopIteration

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
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
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

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
