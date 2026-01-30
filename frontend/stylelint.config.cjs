module.exports = {
    extends: [
        'stylelint-config-standard',
        'stylelint-config-clean-order',
    ],
    plugins: ['stylelint-order'],
    rules: {
        // разрешаем современные фичи
        'selector-class-pattern': null,
        'keyframes-name-pattern': null,

        // порядок свойств
        'order/properties-order': [],
    },
}
