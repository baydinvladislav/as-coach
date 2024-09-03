import React, { useState } from 'react';
import {
  Image,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from 'react-native';

import { getFoodDetails } from '@api';
import { Screens, useNavigation } from '@navigation';

export const MainScreen: React.FC = () => {
  const [exListIndex, setExListIndex] = useState<number | null>(null);
  const data = getFoodDetails();
  const meals2 = ['breakfast', 'lunch', 'dinner', 'snacks'];
  const meals = Object.keys(getFoodDetails().actual_nutrition).filter(
    item => item != 'daily_total',
  );
  const handlePressMeal = (index: number) => {
    setExListIndex(index === exListIndex ? null : index); // Toggle the selected index
  };

  function fractionToPercentage(numerator: number, denominator: number) {
    if (denominator === 0) {
      return 0;
    }
    return (numerator / denominator) * 100;
  }
  const navigation = useNavigation();

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity>
          <Image
            source={require('../../assets/images/calendar.png')}
            style={{ height: 30, width: 30 }}
          />
        </TouchableOpacity>
        <Text style={styles.headerText}>{data.date}</Text>
        <View style={styles.profilePic} />
      </View>
      <View style={styles.statsContainer}>
        <View style={styles.statsRow}>
          <View style={{ width: '25%', alignItems: 'center' }}>
            <Text style={styles.statsText}>🥩 Proteins</Text>
          </View>
          <View style={{ width: '25%', alignItems: 'center' }}>
            <Text style={styles.statsText}>🌰 Fats</Text>
          </View>
          <View style={{ width: '25%', alignItems: 'center' }}>
            <Text style={styles.statsText}>🌾 Carbs</Text>
          </View>
        </View>
        <View style={styles.progressRow}>
          <View style={styles.progressBar}>
            <View
              style={{
                height: '100%',
                width: `${fractionToPercentage(
                  data?.actual_nutrition.daily_total.proteins_consumed,
                  data.actual_nutrition.daily_total.proteins_total,
                )}%`,
                backgroundColor: '#7856FF',
                borderRadius: 20,
              }}
            />
          </View>
          <View style={styles.progressBar}>
            <View
              style={{
                height: '100%',
                width: `${fractionToPercentage(
                  data?.actual_nutrition.daily_total.fats_consumed,
                  data.actual_nutrition.daily_total.fats_total,
                )}%`,
                backgroundColor: '#7856FF',
                borderRadius: 20,
              }}
            />
          </View>
          <View style={styles.progressBar}>
            <View
              style={{
                height: '100%',
                width: `${fractionToPercentage(
                  data?.actual_nutrition.daily_total.carbs_consumed,
                  data.actual_nutrition.daily_total.carbs_total,
                )}%`,
                backgroundColor: '#7856FF',
                borderRadius: 20,
                // width: '30%',
              }}
            />
          </View>
        </View>
        <View style={styles.statsValuesRow}>
          <View style={styles.statsValueContainer}>
            <Text style={styles.statsValue}>
              {data.actual_nutrition.daily_total.proteins_consumed}
            </Text>
            <Text style={styles.statsTotalValue}>
              {' '}
              / {data.actual_nutrition.daily_total.proteins_total} g
            </Text>
          </View>
          <View style={styles.statsValueContainer}>
            <Text style={styles.statsValue}>
              {data.actual_nutrition.daily_total.fats_consumed}
            </Text>
            <Text style={styles.statsTotalValue}>
              {' '}
              / {data.actual_nutrition.daily_total.fats_total} g
            </Text>
          </View>
          <View style={styles.statsValueContainer}>
            <Text style={styles.statsValue}>
              {data.actual_nutrition.daily_total.carbs_consumed}
            </Text>
            <Text style={styles.statsTotalValue}>
              {' '}
              / {data.actual_nutrition.daily_total.carbs_total} g
            </Text>
          </View>
        </View>
      </View>
      <ScrollView>
        {meals.map((meal, index) => (
          <TouchableOpacity
            activeOpacity={1}
            key={index}
            style={styles.mealTouchable}
            onPress={() => handlePressMeal(index)}
          >
            <View style={styles.mealContainer}>
              <View style={styles.mealHeader}>
                <Text style={styles.mealText}>
                  {meal.charAt(0).toUpperCase() + meal.slice(1)}
                </Text>
                {exListIndex === index && (
                  <Image
                    source={require('../../assets/images/uparrow.png')}
                    style={styles.arrowIcon}
                  />
                )}
              </View>
              <TouchableOpacity
                onPress={() => {
                  navigation.navigate(Screens.FoodSelectionScreen, { meal });
                }}
                style={styles.addButton}
              >
                <Text style={styles.plusText}>+</Text>
              </TouchableOpacity>
            </View>
            {exListIndex === index && (
              <View style={styles.expandedMealContainer}>
                <View style={styles.nutritionFactsRow}>
                  <View style={styles.nutritionFacts}>
                    <Text style={[styles.nutritionFact, { marginLeft: 0 }]}>
                      🍖 {data.actual_nutrition[meal].proteins_consumed}
                    </Text>
                    <Text style={styles.nutritionFact}>
                      🌰 {data.actual_nutrition[meal].fats_consumed}
                    </Text>
                    <Text style={styles.nutritionFact}>
                      🌾 {data.actual_nutrition[meal].carbs_consumed}
                    </Text>
                  </View>
                  <Text style={styles.caloriesText}>
                    🍽️ Calories: {data.actual_nutrition[meal].calories_consumed}
                  </Text>
                </View>
                <View
                  style={{
                    backgroundColor: '#fff',
                    marginTop: '5%',
                    borderBottomWidth: 0.5,
                    borderColor: '#fff',
                    width: '100%',
                  }}
                />
                <View style={{ marginTop: '5%' }}>
                  {[...data.actual_nutrition[meal].products].map(
                    (product, index) => (
                      <TouchableOpacity
                        onPress={() => {
                          navigation.navigate(Screens.FoodDetailsScreen, {
                            product,
                          });
                        }}
                        style={{ marginTop: index == 0 ? '1%' : '7%' }}
                      >
                        <View
                          style={{
                            flexDirection: 'row',
                            width: '100%',
                            justifyContent: 'space-between',
                          }}
                        >
                          <TouchableOpacity
                            disabled={true}
                            activeOpacity={1}
                            onPress={() => {
                              navigation.navigate(Screens.FoodDetailsScreen, {
                                product,
                              });
                            }}
                            key={product.id}
                            style={{ marginBottom: 5 }}
                          >
                            <Text style={styles.mealDetailText}>
                              {product.name}
                            </Text>
                            <Text style={styles.servingSizeText}>
                              {product.amount}g
                            </Text>
                          </TouchableOpacity>
                          <Text
                            style={{
                              color: '#FFFFFF',
                              marginRight: '0%',
                              fontSize: 12,
                            }}
                          >
                            {product?.calories}
                          </Text>
                        </View>
                        <View style={styles.nutritionFactsRow}>
                          <View style={styles.nutritionFacts}>
                            <Text
                              style={[styles.nutritionFact, { marginLeft: 0 }]}
                            >
                              🍖 {product?.proteins}
                            </Text>
                            <Text style={styles.nutritionFact}>
                              🌰 {product?.fats}
                            </Text>
                            <Text style={styles.nutritionFact}>
                              🌾 {product?.carbs}
                            </Text>
                          </View>
                          {/* <Text style={styles.caloriesText}>
                            🍽️ Calories: {product?.calories}
                          </Text> */}
                        </View>
                      </TouchableOpacity>
                    ),
                  )}
                </View>
              </View>
            )}
          </TouchableOpacity>
        ))}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginHorizontal: 10,
    marginTop: 10,
  },
  headerText: {
    color: '#fff',
    fontSize: 20,
  },
  profilePic: {
    width: 40,
    height: 40,
    backgroundColor: '#ccc',
    borderRadius: 20,
  },
  statsContainer: {
    marginVertical: 20,
    backgroundColor: '#2E2D55',
    marginHorizontal: 10,
    borderRadius: 10,
    paddingVertical: 10,
  },
  statsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
  },
  statsText: {
    color: '#fff',
    fontSize: 16,
  },
  progressRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
    paddingHorizontal: 10,
  },
  progressBar: {
    height: 5,
    borderRadius: 30,
    width: '25%',
    backgroundColor: '#555',
    marginTop: 20,
    overflow: 'hidden',
  },
  statsValuesRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
  },
  statsValueContainer: {
    marginTop: 20,
    flexDirection: 'row',
  },
  statsValue: {
    color: '#fff',
    fontSize: 16,
  },
  statsTotalValue: {
    color: 'grey',
    fontSize: 16,
  },
  mealTouchable: {
    backgroundColor: '#333',
    padding: 15,
    marginVertical: 5,
    borderRadius: 10,
  },
  mealContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  mealHeader: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  mealText: {
    color: '#fff',
    fontSize: 18,
  },
  arrowIcon: {
    height: 25,
    width: 25,
    marginLeft: 20,
  },
  addButton: {
    backgroundColor: '#4CAF50',
    height: 30,
    width: 30,
    borderRadius: 15,
    alignItems: 'center',
    justifyContent: 'center',
  },
  plusText: {
    color: '#fff',
    fontSize: 18,
  },
  expandedMealContainer: {
    paddingVertical: 10,
    marginTop: 5,
  },
  nutritionFactsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  nutritionFacts: {
    flexDirection: 'row',
    alignItems: 'center',
    // marginVertical: 15,
  },
  nutritionFact: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '500',
    marginLeft: 10,
  },
  caloriesText: { color: '#fff', fontSize: 14, fontWeight: '500' },
  mealDetailText: { color: '#fff', fontSize: 17, fontWeight: '500' },
  servingSizeText: {
    color: '#B8FF5F',
    fontSize: 14,
    fontWeight: '500',
    marginTop: 5,
  },
});
