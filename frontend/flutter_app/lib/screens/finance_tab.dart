import 'package:flutter/material.dart';
import '../services/api_service.dart';

class FinanceTab extends StatefulWidget {
  final ApiService apiService;
  
  const FinanceTab({super.key, required this.apiService});

  @override
  State<FinanceTab> createState() => _FinanceTabState();
}

class _FinanceTabState extends State<FinanceTab> {
  List<dynamic> _transactions = [];
  Map<String, dynamic>? _summary;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    try {
      final [transactions, summary] = await Future.wait([
        widget.apiService.getTransactions(),
        widget.apiService.getFinancialSummary(),
      ]);
      setState(() {
        _transactions = transactions;
        _summary = summary;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
    }
  }

  Future<void> _addTransaction() async {
    final typeController = TextEditingController();
    final categoryController = TextEditingController();
    final amountController = TextEditingController();
    final descriptionController = TextEditingController();
    
    final result = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Add Transaction'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: typeController,
                decoration: const InputDecoration(labelText: 'Type (income/expense/investment)'),
              ),
              TextField(
                controller: categoryController,
                decoration: const InputDecoration(labelText: 'Category'),
              ),
              TextField(
                controller: amountController,
                decoration: const InputDecoration(labelText: 'Amount'),
                keyboardType: TextInputType.number,
              ),
              TextField(
                controller: descriptionController,
                decoration: const InputDecoration(labelText: 'Description'),
                maxLines: 2,
              ),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Add'),
          ),
        ],
      ),
    );

    if (result == true && typeController.text.isNotEmpty && amountController.text.isNotEmpty) {
      try {
        await widget.apiService.createTransaction({
          'transaction_type': typeController.text,
          'category': categoryController.text,
          'amount': double.parse(amountController.text),
          'description': descriptionController.text.isEmpty ? null : descriptionController.text,
        });
        _loadData();
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Error creating transaction: $e')),
          );
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : Column(
              children: [
                if (_summary != null)
                  Container(
                    padding: const EdgeInsets.all(16),
                    color: Colors.blue.shade50,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Financial Summary (Last 30 Days)',
                          style: Theme.of(context).textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceAround,
                          children: [
                            _SummaryCard(
                              label: 'Income',
                              value: '\$${_summary!['total_income']?.toStringAsFixed(2) ?? '0.00'}',
                              color: Colors.green,
                            ),
                            _SummaryCard(
                              label: 'Expenses',
                              value: '\$${_summary!['total_expenses']?.toStringAsFixed(2) ?? '0.00'}',
                              color: Colors.red,
                            ),
                            _SummaryCard(
                              label: 'Balance',
                              value: '\$${_summary!['net_balance']?.toStringAsFixed(2) ?? '0.00'}',
                              color: Colors.blue,
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                Expanded(
                  child: _transactions.isEmpty
                      ? Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Icon(Icons.account_balance_outlined, size: 64, color: Colors.grey),
                              const SizedBox(height: 16),
                              const Text('No transactions yet'),
                              const SizedBox(height: 8),
                              ElevatedButton(
                                onPressed: _addTransaction,
                                child: const Text('Add Your First Transaction'),
                              ),
                            ],
                          ),
                        )
                      : ListView.builder(
                          padding: const EdgeInsets.all(16),
                          itemCount: _transactions.length,
                          itemBuilder: (context, index) {
                            final transaction = _transactions[index];
                            final isIncome = transaction['transaction_type'] == 'income';
                            final isExpense = transaction['transaction_type'] == 'expense';
                            
                            return Card(
                              margin: const EdgeInsets.only(bottom: 12),
                              child: ListTile(
                                leading: Icon(
                                  isIncome ? Icons.arrow_downward : Icons.arrow_upward,
                                  color: isIncome ? Colors.green : Colors.red,
                                ),
                                title: Text(transaction['category'] ?? ''),
                                subtitle: Text(transaction['description'] ?? ''),
                                trailing: Text(
                                  '${isIncome ? '+' : '-'}\$${transaction['amount']?.toStringAsFixed(2) ?? '0.00'}',
                                  style: TextStyle(
                                    color: isIncome ? Colors.green : Colors.red,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                            );
                          },
                        ),
                ),
              ],
            ),
      floatingActionButton: FloatingActionButton(
        onPressed: _addTransaction,
        child: const Icon(Icons.add),
      ),
    );
  }
}

class _SummaryCard extends StatelessWidget {
  final String label;
  final String value;
  final Color color;

  const _SummaryCard({
    required this.label,
    required this.value,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          value,
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
            color: color,
          ),
        ),
        Text(
          label,
          style: const TextStyle(fontSize: 12),
        ),
      ],
    );
  }
}

