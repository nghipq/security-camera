import React from 'react'
import {View, Text, StyleSheet} from 'react-native'

export default function Animals(props) {
    return(
        <View style={styles.containner}>
            <Text>Animals</Text>
        </View>
    )
}

const styles = StyleSheet.create({
    containner: {
        backgroundColor: "#BBEEB9",
        height: 600,
    }
})