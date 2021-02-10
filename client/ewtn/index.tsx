import angular from 'angular';
import {startApp} from 'superdesk-core/scripts/index';

setTimeout(() => {
    startApp([
        {
            id: 'markForUser',
            load: () => import('superdesk-core/scripts/extensions/markForUser/dist/src/extension').then((res) => res.default),
        },
    ], {});
});

export default angular.module('ewtn', []);
