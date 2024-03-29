/**
 * This is the default configuration file for the Superdesk application. By default,
 * the app will use the file with the name "superdesk.config.js" found in the current
 * working directory, but other files may also be specified using relative paths with
 * the SUPERDESK_CONFIG environment variable or the grunt --config flag.
 */
module.exports = function(grunt) {
    return {
        apps: [
            'superdesk-publisher',
            'superdesk-planning',
            'ewtn'
        ],
        importApps: [
            'superdesk-publisher',
            'superdesk-planning',
            '../ewtn'
        ],
        defaultRoute: '/workspace/personal',
        validatorMediaMetadata: {
            headline: {
                required: true
            },
            alt_text: {
                required: true
            },
            description_text: {
                required: true
            },
            copyrightholder: {
                required: false
            },
            byline: {
                required: false
            },
            usageterms: {
                required: false
            },
            copyrightnotice: {
                required: false
            }
        },

        publisher: {
            protocol: 'https',
            tenant: process.env.PUBLISHER_API_SUBDOMAIN || '',
            domain: process.env.PUBLISHER_API_DOMAIN || 'localhost',
            base: 'api/v2',
            wsDomain: process.env.PUBLISHER_WS_DOMAIN || process.env.PUBLISHER_API_DOMAIN,
            wsPath: process.env.PUBLISHER_WS_PATH || '',
            wsPort: process.env.PUBLISHER_WS_PORT || '8080',
            hideContentRoutesInPublishPane: true,
            hideCustomRoutesInPublishPane: true
        },

        langOverride: {
            'en': {
                'ANPA Category': 'Category',
                'ANPA CATEGORY': 'CATEGORY'
            }
        },

        shortTimeFormat: 'MM/DD/YYYY, h:mm a',
        shortDateFormat: 'MM/DD/YYYY, h:mm a',
        shortWeekFormat: 'MM/DD/YYYY, h:mm a',

        view: {
            timeformat: 'h:mm a',
            dateformat: 'MM/DD/YYYY'
        },

        features: {
            preview: 1,
            swimlane: {columnsLimit: 4},
            editor3: true,
            editorHighlights: true,
            nestedItemsInOutputStage: true,
            customAuthoringTopbar: {
                toDesk: false,
                publish: false,
                publishAndContinue: false,
            },
            elasticHighlight: true,
            planning: true,
            searchShortcut: true,
        },
        workspace: {
            analytics: true,
            planning: true,
            assignments: true,
        },

        ui: {
            sendEmbargo: false,
            publishEmbargo: false,
        },
        
        list: {
            priority: ['priority', 'urgency'],
            firstLine: ['wordcount', 'slugline', 'associations', 'headline', 'byline',
            { 
                field: 'authors',
                options: {
                    displayField: 'username',
                    includeRoles: ['writer', 'photographer'],
                },
            },
            'versioncreated'],
            secondLine: ['profile', 'state', 'source', 'byline', 'copyrightholder', 'usageterms', 'scheduledDateTime', 'update', 'updated', 'category', 'provider', 'expiry', 'desk', 'associatedItems']
        },

        item_profile: {
            change_profile: 1
        },

        search_cvs: [], 
        search: {
            slugline: 1,
            headline: 1,
            unique_name: 1,
            story_text: 1,
            byline: 1,
            keywords: 1,
            creator: 1,
            from_desk: 1,
            to_desk: 1,
            spike: 1,
            scheduled: 1,
            company_codes: 0,
            ingest_provider: 1,
            marked_desks: 1,
            featuremedia: 1,
        },

        gridViewFields: [
            'source',
            'byline',
            'copyrightholder',
            'usageterms',
        ],
    };
};
