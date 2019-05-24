// import App from './components/App';

import React from 'react';
import { createStore } from 'redux';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import App from './components/App';
import { rootReducer } from './store/reducers';

const store = createStore(rootReducer);

ReactDOM.render(
                <Provider store={store}>
                    <App/>
                </Provider>
                ,document.getElementById('app'))


module.hot.accept();