
// business logic

function groupBy(list, keyGetter) {
  const map = new Map();
  list.forEach((item) => {
      const key = keyGetter(item);
      const collection = map.get(key);
      if (!collection) {
          map.set(key, [item]);
      } else {
          collection.push(item);
      }
  });
  return map;
}


export default {
  sum (arr, name) {
    return arr.reduce((accumulator, currentValue) =>
      accumulator + currentValue[name], 0)
  },
  aggregateBy (arr, group_key) {
    let grouped = groupBy(arr, i => i[group_key])
    let result = []
    for (let k of grouped) {
      result.push({
        id: k[0],
        apps: k[1].length,
        player_label: k[1][0]['player_label'],
        player_id: k[1][0]['player'],
        starter: this.sum(k[1], 'starter'),
        minutes: this.sum(k[1], 'minutes'),
        num_goals: this.sum(k[1], 'num_goals'),
        num_assists: this.sum(k[1], 'num_assists'),
        num_shots: this.sum(k[1], 'num_shots'),
        corners: this.sum(k[1], 'corners'),
        yellow_cards: this.sum(k[1], 'yellow_cards'),
        red_cards: this.sum(k[1], 'red_cards'),
        subbed_due_to_injury: this.sum(k[1], 'subbed_due_to_injury')
      })
    }
  return result
  },
  aggregateByPlayer (arr)  {
    return this.aggregateBy(arr, 'player_label')
  },
  aggregateByCompetition (arr) {
    let grouped = groupBy(arr, i => i['match']['competition_name'])
    let result = []
    for (let k of grouped) {
      result.push({
        id: k[0],
        apps: k[1].length,
        date_time: k[1][0]['match']['date_time'],
        competition_id: k[1][0]['match']['competition_id'],
        player_label: k[1][0]['player_label'],
        starter: this.sum(k[1], 'starter'),
        minutes: this.sum(k[1], 'minutes'),
        num_goals: this.sum(k[1], 'num_goals'),
        num_assists: this.sum(k[1], 'num_assists'),
        num_shots: this.sum(k[1], 'num_shots'),
        corners: this.sum(k[1], 'corners'),
        yellow_cards: this.sum(k[1], 'yellow_cards'),
        red_cards: this.sum(k[1], 'red_cards'),
        subbed_due_to_injury: this.sum(k[1], 'subbed_due_to_injury')
      })
    }
  return result
  },

}
