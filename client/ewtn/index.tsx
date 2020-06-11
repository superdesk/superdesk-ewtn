import angular from 'angular';
import {startApp} from 'superdesk-core/scripts/index';
import markForUserExtension from 'superdesk-core/scripts/extensions/markForUser/dist/src/extension';

setTimeout(() => {
    startApp([
        markForUserExtension,
    ], {});
});

export default angular.module('ewtn', []);
