import angular from 'angular';
import {startApp} from 'superdesk-core/scripts/index';

setTimeout(() => {
    startApp([
        {
            id: 'markForUserExtension',
            load: () => import('superdesk-core/scripts/extensions/markForUser'),
        },
        {
            id: 'planning-extension',
            load: () => import('superdesk-planning/client/planning-extension'),
        },
    ], {});
});

export default angular.module('ewtn', []);
