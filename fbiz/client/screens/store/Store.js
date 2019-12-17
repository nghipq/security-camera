import React from 'react'
import {View, Text, StyleSheet} from 'react-native'

export default function Store(props) {
    return(
        <View style={styles.containner}>
            <Text>Store</Text>
        </View>
    )
}

const styles = StyleSheet.create({
    containner: {
        backgroundColor: "#BBEEB9",
        height: 600,
    }
})