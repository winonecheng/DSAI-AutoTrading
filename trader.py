import pandas as pd


def determine_actions(stock_data):
    global status
    status = 0
    actions = list()
    stock_trend = 0
    yesterday_price = stock_data.loc[0]['close']

    for price in stock_data['close']:
        if price < yesterday_price:
            if stock_trend >= 0:
                stock_trend = 0

            action = -1 if stock_trend == 0 and is_valid(-1) else 0
            stock_trend += -1

        elif price > yesterday_price:
            if stock_trend <= 0:
                stock_trend = 0

            action = 1 if stock_trend == 0 and is_valid(1) else 0
            stock_trend += 1

        else:
            action = 0

        actions.append(action)
        yesterday_price = price

    # skip the last day action
    actions = actions[:-1]
    return actions


def is_valid(action):
    global status
    status += action

    if status > 1 or status < -1:
        status -= action
        return 0
    return 1


if __name__ == '__main__':
    # You should not modify this part.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--training',
                       default='training_data.csv',
                       help='input training data file name')
    parser.add_argument('--testing',
                        default='testing_data.csv',
                        help='input testing data file name')
    parser.add_argument('--output',
                        default='output.csv',
                        help='output file name')
    args = parser.parse_args()

    testing_data = pd.read_csv(args.testing, header=None,
                               names=['open', 'high', 'low', 'close'])

    actions = determine_actions(testing_data)
    df = pd.DataFrame(actions)
    df.to_csv(args.output, index=False, header=False)
